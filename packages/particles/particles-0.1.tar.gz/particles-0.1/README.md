# particles #

Sequential Monte Carlo in python. 

## Motivation ##

This package was developed to complement the forthcoming book:

An introduction to Sequential Monte Carlo
Nicolas Chopin and Omiros Papaspiliopoulos

## Features ##

This package is intended to be modular, extensible, and feature-rich. The
following methods are implemented: 

* resampling: multinomial, residual, stratified, systematic and SSP. 

* particle filtering: bootstrap filter, guided filter, APF.

* possibility to define a  state-space model using some (basic) form of 
  probabilistic programming; see below for an example. 

* SQMC (Sequential quasi Monte Carlo);  routines for computing the Hilbert curve, 
  and generating RQMC sequences. 

* particle smoothing: on-line smoothing, FFBS (forward filtering, backward
  sampling), two-filter smoothing. O(N) and O(N^2) variants. 
  FFBS for SQMC is also implemented. 

* Kalman filtering and smoothing. 

* SMC samplers: IBIS, SMC tempering, IBIS (a.k.a. data tempering). 

* Bayesian parameter inference for state-space models: PMMC (PMMH, Particle Gibbs) 
  and SMC^2. 

* Basic support for parallel computation (i.e. running multiple SMC algorithms 
on different CPU cores). 

### Example

Here is how you may define a parametric state-space model: 

```python
class ToySSM(ssm.StateSpaceModel):
    def PX0(self):  # Distribution of X_0 
        return dists.Normal()  # X_0 ~ N(0, 1)
    def PX(self, t, xp):  # Distribution of X_t given X_{t-1}
        return dists.Normal(loc=xp)  # X_t ~ N( X_{t-1}, 1)
    def PY(self, t, xp, x):  # Distribution of Y_t given X_t (and X_{t-1}) 
        return dists.Normal(loc=x, scale=self.sigma)  # Y_t ~ N(X_t, sigma^2)
```

You may now choose a particular model within this class, and simulate data from it:

```python
my_model = ToySSM(sigma=0.2)
x, y = my_model.simulate(200)  # sample size is 200
```

To run a bootstrap particle filter for this model and data `y`, simply do:

```python
alg = particles.SMC(fk=ssm.Bootstrap(ssm=my_model, data=y), N=200)
alg.run()
```

That's it! Head to the documentation for more examples, explanations, 
and installation instructions. 

### Who do I talk to? ###

Nicolas Chopin (nicolas.chopin@ensae.fr) is the main author, contributor, and 
person to blame if things do not work as expected. 

Bug reports, feature requests, questions, rants, etc are welcome, preferably 
on the github page. 
