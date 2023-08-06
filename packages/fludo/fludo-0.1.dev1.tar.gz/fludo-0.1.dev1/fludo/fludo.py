# Fludo, a lightweight e-liquid calculator package for Python 3.
# Copyright (C) 2018 Zsolt Nagy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


class Liquid:
    '''Liquid made of PG and VG (and/or water), optional nicotine concentration in mg/ml and optional name.
If only PG or VG are given, the other is implicitly calculated to give 100 percent.
If both are given, then the sum of the two can't exceed 100 percent, but if it's less, the rest is considered to be water.
Use PG = VG = 0 to make pure water.'''
    def __init__(self, ml=0, nic=0, name='', **kwargs):
        # Check arguments
        if type(ml) not in [int, float]:
            raise TypeError('Volume (ml) has to be either int or float, but given: %s' % str(type(ml)))
        if ml < 0:
            raise ValueError('Volume (ml) has to be a positive number, but given: %s' % ml)
        
        try:
            if type(kwargs['pg']) not in [int, float]:
                raise TypeError('PG percentage has to be either int or float, but given: %s' % str(type(kwargs['pg'])))
            if kwargs['pg'] < 0 or kwargs['pg'] > 100:
                raise ValueError('PG has to be a percentage between 0 and 100, but given: %s' % kwargs['pg'])
        except KeyError:
            pass
        
        try:
            if type(kwargs['vg']) not in [int, float]:
                raise TypeError('VG percentage has to be either int or float, but given: %s' % str(type(kwargs['vg'])))
            if kwargs['vg'] < 0 or kwargs['vg'] > 100:
                raise ValueError('VG has to be a percentage between 0 and 100, but given: %s' % kwargs['vg'])
        except KeyError:
            pass
        
        try:
            if kwargs['pg'] + kwargs['vg'] > 100:
                raise ValueError('The sum of PG and VG can not be more than 100 percent, given: %sPG/%sVG' % (kwargs['pg'], kwargs['vg']))
        except KeyError:
            # So we don't have both PG and VG given
            pass
        
        if type(nic) not in [int, float]:
            raise TypeError('Nicotine concentration has to be either int or float, but given: %s' % str(type(nic)))
        if nic < 0:
            raise ValueError('Nicotine concentration has to be a positive number, but given: %s' % nic)
        
        if type(name) not in [str]:
            raise TypeError('Name has to be a string, but given: %s' % str(type(name)))
        
        self.ml = ml
        self.nic = nic

        # Calculate PG/VG percentages and volumes
        try:
            self.pg = kwargs['pg']
            self.vg = kwargs['vg']
        except KeyError:
            try:
                self.pg = kwargs['pg']
                self.vg = 100 - self.pg
            except KeyError:
                try:
                    self.vg = kwargs['vg']
                    self.pg = 100 - self.vg
                    print('VG given')
                except KeyError:
                    # Neither PG nor VG was given, assume 50/50
                    self.pg = self.vg = 50
        
        self.update_ml(self.ml)

        self.name = name if name else type(self).__name__
    
    def update_ml(self, ml):
        self.ml = ml

        self.total_pgml = self.ml * (self.pg / 100)
        self.total_vgml = self.ml * (self.vg / 100)
        
        # Calc nicotine mass
        self.total_nicmg = self.nic * self.ml

    def properties(self, ml=None):
        return {
            'ml': self.ml,
            'pg': self.pg,
            'vg': self.vg,
            'nic': self.nic,
            'name': self.name,
            'type': type(self).__name__
        }

    def __repr__(self):
        return '<%(type)s (%(name)s): %(ml).1f ml, %(pg)dPG/%(vg)dVG, %(nic).1f mg/ml>' % self.properties()


class Water(Liquid):
    def __init__(self, ml, **kwargs):
        # Require ml
        if 'pg' in kwargs or 'vg' in kwargs or 'nic' in kwargs:
            raise NameError('Can not have PG/VG percentage or Nic for Water.')
        super().__init__(ml, pg=0, vg=0, nic=0, **kwargs)
        try:
            name
        except NameError:
            self.name = Water.__name__
    
    def __repr__(self):
        return '<%(type)s (%(name)s): %(ml).1f ml>' % self.properties()


class Base(Liquid):
    def __init__(self, ml, **kwargs):
        # Require ml
        super().__init__(ml, **kwargs)
        if self.pg + self.vg < 100:
            raise ValueError('PG and VG sum for Base should be 100.')
        try:
            name
        except NameError:
            self.name = Base.__name__
    
    def __repr__(self):
        return '<%(type)s (%(name)s): %(ml).1f ml, %(pg)dPG/%(vg)dVG>' % self.properties()


class NicBase(Liquid):
    def __init__(self, ml, nic, **kwargs):
        # Require ml, nic
        super().__init__(ml, nic=nic, **kwargs)
        try:
            name
        except NameError:
            self.name = NicBase.__name__


class Aroma(Liquid):
    def __init__(self, ml, name, **kwargs):
        # Require ml, name
        super().__init__(ml, name=name, **kwargs)
    
    def __repr__(self):
        return '<Aroma (%(name)s): %(ml).1f ml, %(pg)dPG/%(vg)dVG>' % self.properties()


class Mixture(Liquid):
    ''' Used to mix liquids together. '''
    def __init__(self, *components):
        super().__init__(0)

        self.components = []

        # Add components if got any as arguments
        if components:
            for component in components:
                self.add(component)

    def add(self, *components):
        ''' Add liquids to the mixture. '''
        for component in components:
            if not isinstance(component, Liquid):
                raise TypeError('Can only add Liquids, but given: %s' % str(type(component)))
            if component.ml > 0:
                if not isinstance(component, Mixture):
                    # Got liquid, not a mixture

                    # Volume addition and PG/VG recalculation
                    self.ml += component.ml
                    self.total_pgml += component.total_pgml
                    self.total_vgml += component.total_vgml
                    self.pg = (self.total_pgml / self.ml) * 100
                    self.vg = (self.total_vgml / self.ml) * 100

                    # Nicotine mass addition
                    self.total_nicmg += component.total_nicmg

                    # Recalculate nicotine concentration in total volume
                    self.nic = self.total_nicmg / self.ml

                    self.components.append(component)
                else:
                    # Got mixture
                    self.add(*component.components)
        
        return self
    
    def pour(self, amount):
        ''' Returns an instance of mixture of some amount with the same ratio of components. '''
        if self.ml > 0:
            return Mixture(*[component.__class__(component.ml * (amount / self.ml),
                pg=component.pg,
                vg=component.vg,
                nic=component.nic,
                name=component.name) for component in self.components])
        else:
            raise Exception('Can not pour from a 0 ml mixture.')
