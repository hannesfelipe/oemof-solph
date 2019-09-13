# -*- coding: utf-8 -*-

""" Classes used to model energy supply systems within
oemof's solver for convex optimization problems (scoop)

Classes are derived from oemof core network classes and adapted for specific
optimization tasks. An energy system is modelled as a graph/network of nodes
with very specific constraints on which types of nodes are allowed to be
connected.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/network.py

SPDX-License-Identifier: GPL-3.0-or-later

Copyright (c) Patrik Schönfeldt
Copyright (c) DLR Institute of Networked Energy Systems
"""

import cvxpy

import oemof.network as on
import oemof.energy_system as es


class Flow(on.Edge):
    r"""
    Defines a flow between two nodes.
    
    """

    def __init__(self, **kwargs):
        super().__init__()

        scalars = ['nominal_value']
        keys = [k for k in kwargs if k != 'label']

        for attribute in set(scalars + sequences + keys):
            value = kwargs.get(attribute, defaults.get(attribute))
            setattr(self, attribute,
                    sequence(value) if attribute in sequences else value)


    def constraint_group(self):
        if not self.actual_value:
            self.actual_value = cp.Variable(model.number_of_timesteps)
            return [self.actual_value <= self.nominal_value]
        else:
            return None



class Bus(on.Bus):
    r"""
    A balance object.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.balanced = kwargs.get('balanced', True)


    def constraint_group(self):
        if self.balanced:
            return [sum(i for i in self.in_flows) == sum(o for o in out_flows)]
        else:
            return None

class Sink(on.Sink):
    """An object with one input flow.
    """
    def constraint_group(self):
        pass

class Source(on.Source):
    """An object with one output flow.
    """
    def constraint_group(self):
        pass


class Transformer(on.Transformer):
    r"""
    A linear Transformer object with n inputs and n outputs.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys are the connected bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}

        missing_conversion_factor_keys = (
            (set(self.outputs) | set(self.inputs)) -
            set(self.conversion_factors))

        for cf in missing_conversion_factor_keys:
            self.conversion_factors[cf] = sequence(1)


    def constraint_group(self):
        for o in out_flows:
            for i in in_flows:
                try:
                    lhs = (i[t] / n.conversion_factors[i][t])
                    rhs = (o[t] / n.conversion_factors[o][t])
        return [lhs == rhs]


