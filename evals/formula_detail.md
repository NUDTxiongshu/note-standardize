# Formula detail test source

## AR(1)

The centered AR(1) model is

$$x_t=\phi_0+\phi_1x_{t-1}+\varepsilon_t$$

where \(\phi_0\) is the intercept, \(\phi_1\) is the coefficient on the previous observation, and \(\varepsilon_t\) is white noise with \(E(\varepsilon_t)=0\), \(Var(\varepsilon_t)=\sigma^2\). Assume \(\phi_1\ne 1\) and \(E(x_s\varepsilon_t)=0\) for \(s<t\). For a stationary process, let \(E(x_t)=E(x_{t-1})=\mu\). Taking expectations in the model gives

$$\mu=\phi_0+\phi_1\mu+0.$$

Move the lagged-mean term to the left:

$$\mu(1-\phi_1)=\phi_0,$$

so

$$\mu=\frac{\phi_0}{1-\phi_1}.$$

The intercept shifts the long-run mean; when \(\phi_0=0\), the process is centered and its mean is zero.

## MA(1)

Use the plus-sign convention

$$x_t=\varepsilon_t+\theta\varepsilon_{t-1},$$

where \(\varepsilon_t\) is zero-mean white noise with variance \(\sigma^2\), and innovations at different times are uncorrelated. Then \(E(x_t)=0\). In the variance, the two innovation terms are from different times and their covariance is zero:

$$Var(x_t)=\sigma^2(1+\theta^2).$$

At lag one, \(x_t\) and \(x_{t-1}\) share \(\varepsilon_{t-1}\), so

$$\gamma_1=Cov(x_t,x_{t-1})=\theta\sigma^2,\qquad \rho_1=\frac{\theta}{1+\theta^2}.$$

For lags \(k\ge2\), the two observations share no innovation, hence \(\gamma_k=\rho_k=0\). This is why the theoretical ACF of MA(1) cuts off after lag one.