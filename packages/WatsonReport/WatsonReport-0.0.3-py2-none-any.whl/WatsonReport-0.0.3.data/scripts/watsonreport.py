import subprocess
import shlex
import pandas as pd
import json
import sys
import tempfile
fromDate = sys.argv[-1]
command = "watson log -f %s -j" % fromDate
output = json.loads(subprocess.check_output(shlex.split(command)))

df = pd.DataFrame(output)
df.start = pd.to_datetime(df.start)
df.stop = pd.to_datetime(df.stop)
df['delta'] = (df.stop - df.start)
outputfile = tempfile.mktemp(suffix='.xlsx')
result = df[['project', 'delta']].groupby(['project', df.start.dt.date]).sum().unstack().reset_index().set_index('project').sort_index()
result.to_excel(outputfile)
print result
print outputfile


