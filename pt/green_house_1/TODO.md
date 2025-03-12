
# Pending Tasks

1. Refactor and test the code.
2. Introduce config based on DTaaS yaml specification. Use py-yaml
3. Integrate [Oslo greenhouse actuator](https://github.com/MarcoAmato/greenhouse_actuator)
   into this example.

## Further Ideas

Use [autoregressive exogenous input (ARX) models](https://apmonitor.com/dde/index.php/Main/AutoRegressive)
for soil modeling.
The python [statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.tsa.ar_model.AutoReg.html)
package for this purpose.

See [example](https://colab.research.google.com/github/APMonitor/dde/blob/main/ARX_Model.ipynb).
