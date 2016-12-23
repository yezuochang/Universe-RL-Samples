#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 vishalapr <vishalapr@vishal-Lenovo-G50-70>
#
# Distributed under terms of the MIT license.

"""

"""

import gym
import universe

import time
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

load_model = 1
backup_iter = 18
save_iter = 5

# Reinforcement Learning - Deep-Q learning
model = Sequential()
model.add(Dense(32, input_dim=4, init='uniform', activation='sigmoid'))
model.add(Dense(64, init='glorot_uniform', activation='sigmoid'))
model.add(Dense(2, init='glorot_uniform', activation='sigmoid'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

if load_model == 1:
	model.load_weights("cartpole.keras")

env = gym.make('CartPole-v0')
replay_memory = []
gamma = 0.98

for episode in range(100000):
	observation = env.reset()
	observation = np.reshape(observation, [1, 4])	
	for time_t in range(10000):
		env.render()
		# Action space is either 0 or 1 for cartpole
		# print env.action_space
		action = model.predict(observation)
		action = np.argmax(action[0])	
		if np.random.uniform(0,1) < 0.3:
			# Either 0 or 1 sample the action randomly
			action = np.random.randint(2)
		# print observation, action
		#action = env.action_space.sample()
		#print action
		observation_old = observation
		observation, reward, done, info = env.step(action)
		observation = np.reshape(observation, [1, 4])
		replay_memory.append([observation_old, action, reward, observation])
		if done:
			print 'Episode finished'
			break
	for mem in replay_memory[:-1]:
		target = mem[2] + gamma * np.amax(model.predict(observation)[0])
		print target
		target_f = model.predict(observation_old)
		target_f[0][np.argmax(target_f[0])] = target
		model.fit(observation_old, target_f, nb_epoch=1)
	if episode % save_iter == 0:
		model.save_weights("cartpole.keras")
	if episode % backup_iter == 0:
		model.save_weights("cartpole_backup.keras")

