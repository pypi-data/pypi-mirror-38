import pandas as pd
from itertools import chain, tee, combinations
from functools import reduce
from operator import mul
from collections import defaultdict, Counter
import random
import time
import numpy as np
import copy
import json
import os

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def show_time(func):

	"""
	timer decorator
	"""

	def wrapper(*args, **kwargs):

		t0 = time.time()
		v = func(*args, **kwargs)
		print('elapsed time: {:.0f} min {:.0f} sec'.format(*divmod(time.time() - t0, 60)))

		return v

	return wrapper

class MTA:

	def __init__(self, data='data.csv.gz', allow_loops=False):

		self.data = pd.read_csv(os.path.join('data', data))

		if not (set(self.data.columns) <= set('path total_conversions total_conversion_value total_null'.split())):
			raise ValueError(f'wrong column names in {data}!')

		if not allow_loops:
			self.remove_loops()

		#split journey into a list of visited channels
		self.data['path'] = self.data['path'].str.split('>').apply(lambda _: [ch.strip() for ch in _]) 
		# make a sorted list of channel names
		self.channels = sorted(list({ch for ch in chain.from_iterable(self.data['path'])}))
		# add some extra channels
		self.channels_ext = ['(start)'] + self.channels + ['(conversion)', '(null)']
		# make dictionary mapping a channel name to it's index
		self.c2i = {c: i for i, c in enumerate(self.channels_ext)}

		self.m = np.zeros(shape=(len(self.channels_ext), len(self.channels_ext)))
		self.removal_effects = defaultdict(float)

		self.attribution = defaultdict(lambda: defaultdict(float))

	def show_data(self):

		print(f'rows: {len(self.data):,}')
		print(f'channels: {len(self.channels)}')
		print(f'conversions: {self.data["total_conversions"].sum():,}')
		print(f'exits: {self.data["total_null"].sum():,}')
		print('sample:')
		print(self.data.head())

		return self

	def remove_loops(self):

		"""
		remove transitions from a channel directly to itself, e.g. a > a
		"""

		cpath = []

		for row in self.data.itertuples():

			clean_path = []

			for i, p in enumerate([w.strip() for w in row.path.split('>')], 1):

				if i == 1:
					clean_path.append(p)
				else:
					if p != clean_path[-1]:
						clean_path.append(p)

			cpath.append(' > '.join(clean_path))

		self.data_ = pd.concat([pd.DataFrame({'path': cpath}), 
								self.data[[c for c in self.data.columns if c != 'path']]], axis=1)

		self.data = self.data_.groupby('path').sum().reset_index()

		return self

	def normalize_dict(self, d):
		"""
		returns a value-normalized version of dictionary d
		"""
		sum_all_values = sum(d.values())

		for _ in d:
			d[_] = round(d[_]/sum_all_values, 6)

		return d

	def linear(self, share='same', normalize=True):

		"""
		either give exactly the same share of conversions to each visited channel (option share=same) or
		distribute the shares proportionally, i.e. if a channel 1 appears 2 times on the path and channel 2 once
		then channel 1 will receive double credit

		note: to obtain the same result as ChannelAttbribution produces for the test data set, you need to

			- select share=proportional
			- allow loops - use the data set as is without any modifications
		"""

		if share not in 'same proportional'.split():
			raise ValueError('share parameter must be either *same* or *proportional*!')

		self.linear = defaultdict(float)

		for row in self.data.itertuples():

			if row.total_conversions:

				if share == 'same':

					n = len(set(row.path))    # number of unique channels visited during the journey
					s = row.total_conversions/n    # each channel is getting an equal share of conversions

					for c in set(row.path):
						self.linear[c] += s

				elif share == 'proportional':

					c_counts = Counter(row.path)  # count how many times channels appear on this path
					tot_appearances = sum(c_counts.values())

					c_shares = defaultdict(float)

					for c in c_counts:

						c_shares[c] = c_counts[c]/tot_appearances

					for c in set(row.path):

						self.linear[c] += row.total_conversions*c_shares[c]

		if normalize:
			self.linear = self.normalize_dict(self.linear)

		self.attribution['linear'] = self.linear

		return self

	def time_decay(self, count_direction='left', normalize=True):

		"""
		time decay - the closer to conversion was exposure to a channel, the more credit this channel gets

		this can work differently depending how you get timing sorted. 

		example: a > b > c > b > a > c > (conversion)
	
		we can count timing backwards: c the latest, then a, then b (lowest credit) and done. Or we could count left to right, i.e.
		a first (lowest credit), then b, then c. 

		"""

		self.time_decay = defaultdict(float)

		if count_direction not in 'left right'.split():
			raise ValueError('argument count_direction must be *left* or *right*!')

		for row in self.data.itertuples():

			if row.total_conversions:

				channels_by_exp_time = []

				_ = row.path if count_direction == 'left' else row.path[::-1]

				for c in _:
					if c not in channels_by_exp_time:
						channels_by_exp_time.append(c)

				if count_direction == 'right':
					channels_by_exp_time = channels_by_exp_time[::-1]

				# first channel gets 1, second 2, etc.

				score_unit = 1./sum(range(1, len(channels_by_exp_time) + 1))

				for i, c in enumerate(channels_by_exp_time, 1):
					self.time_decay[c] += i*score_unit*row.total_conversions

		if normalize:
			self.time_decay = self.normalize_dict(self.time_decay)

		self.attribution['time_decay'] = self.time_decay

		return self

	def first_touch(self, normalize=True):

		first_touch = defaultdict(int)

		for c in self.channels:

			# total conversions for all paths where the first channel was c
			first_touch[c] = self.data.loc[self.data['path'].apply(lambda _: _[0] == c), 'total_conversions'].sum()

		if normalize:
			first_touch = self.normalize_dict(first_touch)

		self.attribution['first_touch'] = first_touch

		return self

	def last_touch(self, normalize=True):

		last_touch = defaultdict(int)

		for c in self.channels:

			# total conversions for all paths where the last channel was c
			last_touch[c] = self.data.loc[self.data['path'].apply(lambda _: _[-1] == c), 'total_conversions'].sum()

		if normalize:
			last_touch = self.normalize_dict(last_touch)

		self.attribution['last_touch'] = last_touch

		return self

	def pairs(self, lst):

		it1, it2 = tee(lst)
		next(it2, None)

		return zip(it1, it2)

	def count_pairs(self):

		"""
		count how many times channel pairs appear on all recorded customer journey paths
		"""

		c = defaultdict(int)

		for row in self.data.itertuples():

			for ch_pair in self.pairs(['(start)'] + row.path):
				c[ch_pair] += (row.total_conversions + row.total_null)

			c[(row.path[-1], '(null)')] += row.total_null
			c[(row.path[-1], '(conversion)')] += row.total_conversions

		return c

	def ordered_tuple(self, t):

		"""
		return tuple t ordered 
		"""

		if not isinstance(t, tuple):
			raise TypeError(f'provided value {t} is not tuple!')

		if all([len(t) == 1, t[0] in '(start) (null) (conversion)'.split()]):
			raise Exception(f'wrong transition {t}!')

		if (len(t) > 1) and (t[-1] == '(start)'): 
			raise Exception(f'wrong transition {t}!')

		if (len(t) > 1) and (t[0] == '(start)'):
			return (t[0],) + tuple(sorted(list(t[1:])))

		if (len(t) > 1) and (t[-1] in '(null) (conversion)'.split()):
			return tuple(sorted(list(t[:-1]))) + (t[-1],)

		return tuple(sorted(list(t)))

	def trans_matrix(self):

		trans_probs = defaultdict(float)

		outs = defaultdict(int)

		# here pairs are unordered
		pair_counts = self.count_pairs()

		for pair in pair_counts:

			outs[pair[0]] += pair_counts[pair]

		for pair in pair_counts:

			trans_probs[pair] = pair_counts[pair]/outs[pair[0]]

		return trans_probs

	@show_time
	def simulate_path(self, n=int(1e6), drop_state=None):

		conv_or_null = defaultdict(int)
		channel_idxs = list(self.c2i.values())

		null_idx = self.c2i['(null)']

		m = copy.copy(self.m)

		if drop_state:

			drop_idx = self.c2i[drop_state]
			# no exit from this state, i.e. it becomes (null)
			m[drop_idx] = 0

		else:

			drop_idx = null_idx

		for _ in range(n):

			init_idx = self.c2i['(start)']
			final_state = None

			while not final_state:

				next_idx = np.random.choice(channel_idxs, p=m[init_idx], replace=False)

				if next_idx == self.c2i['(conversion)']:
					conv_or_null['(conversion)'] += 1
					final_state = True
				elif next_idx in {null_idx, drop_idx}:
					conv_or_null['(null)'] += 1
					final_state = True
				else:
					init_idx = next_idx

		return conv_or_null

	def calculate_removal_effects(self, normalize=True):

		print('calculating removal effects...')

		cvs = defaultdict()  # conversions by channel

		cvs['no_removals'] = self.simulate_path()

		for i, ch in enumerate(self.channels, 1):

			print(f'{i}/{len(self.channels)}: removed channel {ch}...')

			cvs[ch] = self.simulate_path(drop_state=ch)
			self.removal_effects[ch] = round((cvs['no_removals']['(conversion)'] - 
												cvs[ch]['(conversion)'])/cvs['no_removals']['(conversion)'], 6)

		if normalize:
			self.removal_effects = self.normalize_dict(self.removal_effects)

		return self

	def prob_convert(self, trans_mat, drop=None):

		_d = self.data[self.data['path'].apply(lambda x: drop not in x) & (self.data['total_conversions'] > 0)]

		p = 0

		for row in _d.itertuples():

			pr_this_path = []

			for t in self.pairs(['(start)'] + row.path + ['(conversion)']):

				pr_this_path.append(trans_mat.get(t, 0))

			p += reduce(mul, pr_this_path)

		return p


	def markov(self, sim=False, normalize=True):

		markov = defaultdict(float)

		tr = self.trans_matrix()

		p_conv = self.prob_convert(trans_mat=tr)

		for c in self.channels:
			markov[c] = (p_conv - self.prob_convert(trans_mat=tr, drop=c))/p_conv

		if normalize:
			markov = self.normalize_dict(markov)

		self.attribution['markov'] = markov


		return self

	def shao(self, normalize=True):

		"""
		probabilistic model by Shao and Li (supposed to be equivalent to Shapley); explanation in the original paper may seem rather unclear but
		this https://stats.stackexchange.com/questions/255312/multi-channel-attribution-modelling-using-a-simple-probabilistic-model 
		is definitely helpful
		"""

		r = defaultdict(lambda: defaultdict(float))

		# count user conversions and nulls for each visited channel and channel pair

		for row in self.data.itertuples():

			for n in [1,2]:

				for ch in combinations(set(row.path), n):
					
					t = self.ordered_tuple(ch)

					r[t]['(conversion)'] += row.total_conversions
					r[t]['(null)'] += row.total_null

		for _ in r:
			r[_]['conv_prob'] = r[_]['(conversion)']/(r[_]['(conversion)'] + r[_]['(null)'])

		# calculate channel contributions

		self.C = defaultdict(float)

		for row in self.data.itertuples():

			for ch_i in set(row.path):

				if row.total_conversions:

					pc = 0    # contribution for current path

					other_channels = set(row.path) - {ch_i}

					k = 2*len(other_channels) if other_channels else 1 

					for ch_j in other_channels:

						pc += (r[self.ordered_tuple((ch_i, ch_j))]['conv_prob'] - 
														r[(ch_i,)]['conv_prob'] - 
														r[(ch_j,)]['conv_prob'])

					pc = r[(ch_i,)]['conv_prob']  + pc/k

					self.C[ch_i] += row.total_conversions*pc


		if normalize:
			self.C = self.normalize_dict(self.C)

		self.attribution['shao'] = self.C

		return self

	def get_generated_conversions(self, max_subset_size=3):

		self.cc = defaultdict(lambda: defaultdict(float))

		for ch_list, convs, nulls in zip(self.data['path'], 
											self.data['total_conversions'], 
												self.data['total_null']):

			# only look at journeys with conversions
			for n in range(1, max_subset_size + 1):

				for tup in combinations(set(ch_list), n):

					tup_ = self.ordered_tuple(tup)

					self.cc[tup_]['(conversion)'] += convs
					self.cc[tup_]['(null)'] += nulls

		return self

	def v(self, coalition):
		
		"""
		total number of conversions generated by all subsets of the coalition;
		coalition is a tuple of channels
		"""

		s = len(coalition)

		total_convs = 0

		for n in range(1, s+1):
			for tup in combinations(coalition, n):
				tup_ = self.ordered_tuple(tup)
				total_convs += self.cc[tup_]['(conversion)']

		return total_convs

	def w(self, s, n):
		
		return np.math.factorial(s)*(np.math.factorial(n - s -1))/np.math.factorial(n)


	def shapley(self, max_coalition_size=2, normalize=True):

		"""
		Shapley model; channels are players, the characteristic function maps a coalition A to the 
		the total number of conversions generated by all the subsets of the coalition

		see https://medium.com/data-from-the-trenches/marketing-attribution-e7fa7ae9e919
		"""

		self.get_generated_conversions(max_subset_size=3)

		self.phi = defaultdict(float)

		for ch in self.channels:
			# all subsets of channels that do NOT include ch
			for n in range(1, max_coalition_size + 1):
				for tup in combinations(set(self.channels) - {ch}, n):
					self.phi[ch] += (self.v(tup + (ch,)) - self.v(tup))*self.w(len(tup), len(self.channels))

		if normalize:
			self.phi = self.normalize_dict(self.phi)

		self.attribution['shapley'] = self.phi

		return self

	def logistic_regression(self, test_size=0.25, ps=0.5, pc=0.5, normalize=True, n=2000):

		"""
		test_size is the proportion of data set to use as the test set
		ps is the proportion of rows to sample
		pc is the proportion of columns to sample
		n is the number of iterations
		"""

		lr = defaultdict(float)

		# expand the original data set into a feature matrix
		lists_ = []
		flags_ = []

		for i, row in enumerate(self.data.itertuples()):

			for _ in range(row.total_conversions):
				lists_.append({c: 1 for c in row.path})
				flags_.append(1)

			for _ in range(row.total_null):
				lists_.append({c: 1 for c in row.path})
				flags_.append(0)

		data_ = pd.concat([pd.DataFrame(lists_).fillna(0), 
								pd.DataFrame({'conv': flags_})], axis=1).sample(frac=1.0)

		for _ in range(1, n + 1):

			dd = pd.concat([data_[data_['conv'] == 1].sample(frac=0.5), 
							data_[data_['conv'] == 0].sample(frac=0.5)])

			# randomly sample features (channels) and rows (journeys)
			dd = dd.sample(frac=ps)

			dd = pd.concat([dd.drop('conv', axis=1).sample(frac=pc, axis=1), dd['conv']], axis=1)
	
			# split into training/test set
			X_train, X_test, y_train, y_test = train_test_split(dd.drop('conv', axis=1), dd['conv'], 
														test_size=test_size, random_state=36, stratify=dd['conv'])

			# fit logistic regression classifier
			clf = LogisticRegression(random_state=32, solver='lbfgs', fit_intercept=False).fit(X_train, y_train)
	
			# predict conversion labels for the test set
			yh = clf.predict(X_test)

			minc = min(clf.coef_[0])
			maxc = max(clf.coef_[0])

			for c, coef in zip(X_train.columns, [k*k for k in clf.coef_[0]]):
				lr[c] += coef/n

		if normalize:
			lr = self.normalize_dict(lr)

		self.attribution['log_regr'] = lr

		return self

	def show(self):

		"""
		show simulation results
		"""

		res = pd.DataFrame.from_dict(mta.attribution)

		print(res)

if __name__ == '__main__':

	mta = MTA(allow_loops=False)

	mta.linear(share='proportional') \
			.time_decay(count_direction='right') \
			.shapley() \
			.shao() \
			.first_touch() \
			.last_touch() \
			.markov() \
			.logistic_regression()
	