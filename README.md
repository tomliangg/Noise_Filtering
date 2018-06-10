# CMPT353-e3
<h3>This repo is created for documentation purpose. The repo contains my personal work toward the SFU CMPT353 (Computational Data Science) course. You may use my solution as a reference. The .zip archive contains the original exercise files. For practice purpose, you can download the .zip archive and start working from there.</h3>

<p><a href="https://coursys.sfu.ca/2018su-cmpt-353-d1/pages/AcademicHonesty">Academic Honesty</a>: it's important, as always.</p>
<p>Below is the exercise description </p>
<hr>

<div class="wikicontents creole tex2jax_process"><p>Due <span title="2018-06-01T23:59:59-07:00">Friday June 01 2018</span>.</p>
<p>Some files are provided that you need below: <a href="E3.zip">E3.zip</a>. <strong>You may not write any loops</strong> in your code (except in one place mentioned below).</p>
<h2 id="h-cpu-temperature-noise-reduction">CPU Temperature Noise Reduction</h2>
<p>I gathered some data on the CPU temperature and usage of one of the computers in my life: sampling every minute (with <a href="https://pypi.python.org/pypi/psutil">psutil</a>, if you're wondering). That gives a temperature (in <span>&deg;</span>C), CPU usage (in percent), and one-minute system load (number of processes running/waiting averaged over the last minute). The data is in the provided <code>sysinfo.csv</code>.</p>
<p>If you have a look, you will see that there's a certain amount of noise from the temperature sensor, but it also seems like there are some legitimate changes in the true temperature. We would like to separate these as best possible and determine the CPU temperature as closely as we can.</p>
<p>For this question, write a Python program <code>smooth_temperature.py</code>. It should take its input CSV file as a command line argument:</p>
<pre class="highlight lang-bash">python3 smooth_temperature.py sysinfo.csv</pre>
<p>Before you get started, have a look:</p>
<pre class="highlight lang-python">plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.show() # easier for testing
# plt.savefig('cpu.svg') # for final submission</pre>
<h3 id="h-loess-smoothing">LOESS Smoothing</h3>
<p>We can try LOESS smoothing to get the signal out of noise. For this part of the question, we're only worried about the temperature values.</p>
<p>Use the <a href="http://www.statsmodels.org/stable/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html"><code>lowess</code> function from statsmodels</a> to generated a smoothed version of the temperature values.</p>
<p>Adjust the <code>frac</code> parameter to get as much signal as possible with as little noise as possible. The contrasting factors: (1) when the temperature spikes (because of momentary CPU usage), the high temperature values are reality and we don't want to smooth that information out of existence, but (2) when the temperature is relatively flat (where the computer is not in use), the temperature is probably relatively steady, not jumping randomly between 30<span>&deg;</span>C and 33<span>&deg;</span>C as the data implies.</p>
<p>Have a look and see how you're doing:</p>
<pre class="highlight lang-python">loess_smoothed = lowess(…)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')</pre>
<h3 id="h-kalman-smoothing">Kalman Smoothing</h3>
<p>A Kalman filter will let us take more information into account: we can use the processor usage and system load to give a hint about when the temperature will be increasing/decreasing. The time stamp will be distracting: keep only the three columns you need.</p>
<pre class="highlight lang-python">kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1']]</pre>
<p>To get you started on the Kalman filter parameters, I have something like this:</p>
<pre class="highlight lang-python">initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0, 0, 0]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0, 0, 0]) ** 2 # TODO: shouldn't be zero
transition = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] # TODO: shouldn't (all) be zero</pre>
<p>You can choose sensible (non-zero) values for the observation standard deviations here. The value <code>observation_covariance</code> expresses how much you believe the <em>sensors</em>: what kind of error do you usually expect to see (perhaps based on looking at the scatter plot, or by estimating the accuracy of the observed values). The values in the template above are taken to be standard deviations (in the same units as the corresponding values) and then squared to give variance values that the filter expects.</p>
<p>The <code>transition_covariance</code> expresses how accurate <em>your prediction</em> is: how accurately can you predict the temperature of the CPU (and processor percent/load), based on the previous temperature and processor usage?</p>
<p>The transition matrix is where we can be more clever. I predict that the <span>&ldquo;</span>next<span>&rdquo;</span> values of the variables we're observing will be:
\[
\begin{align*}
\mathit{temperature} &amp;\leftarrow 1.0 \times \mathit{temperature} - 1.0\times\mathit{cpu\_percent} + 0.7 \times \mathit{sys\_load\_1} \\
\mathit{cpu\_percent} &amp;\leftarrow 0.6 \times \mathit{cpu\_percent} + 0.03 \times \mathit{sys\_load\_1} \\
\mathit{sys\_load\_1}  &amp;\leftarrow 1.3 \times \mathit{cpu\_percent} + 0.8 \times \mathit{sys\_load\_1}
\end{align*}
\]
These values are the result of doing some regression on the values (and a few manual changes). You're free to change them if you wish, but it's probably not necessary.</p>
<p><strong>Experiment with the parameter values</strong> to get the best smoothed result you can. The tradeoffs are the same as before: removing noise while keeping true changes in the signal. Have a look:</p>
<pre class="highlight lang-python">kf = KalmanFilter(…)
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')</pre>
<h3 id="h-final-output">Final Output</h3>
<p><strong>Add a legend to your plot</strong> so we (and you) can distinguish the data points, LOESS-smoothed line, and Kalman-smoothed line. Hint: you saw <code>plt.legend</code> in Exercise 1.</p>
<p>When you submit, make sure your program is not popping up a window, but <strong>saves the plot as <code>cpu.svg</code></strong> with the data points, LOESS smoothed line, and Kalman smoothed line: <code>plt.savefig('cpu.svg')</code>.</p>
<h2 id="h-gps-tracks-how-far-did-i-walk">GPS Tracks: How Far Did I Walk?</h2>
<p>Sensor noise is a common problem in many areas. One sensor that most of us are carrying around: a GPS receiver in a smartphone (or a smartwatch or other wearable). The data that you get from one of those devices is often filtered automatically to remove noise, but that doesn't mean there isn't noise inherent in the system: GPS <a href="http://www.gps.gov/systems/gps/performance/accuracy/">can be accurate to about 5 m</a> but it seems unlikely that your phone will do that well.</p>
<p>I recorded some tracks of myself walking with <a href="https://play.google.com/store/apps/details?id=com.mendhak.gpslogger&amp;hl=en">GPS Logger for Android</a>. They are included as <code>*.gpx</code> files.</p>
<p>GPX files are XML files that contain (among other things) elements like this for each observation:</p>
<pre class="highlight lang-xml">&lt;trkpt lat="49.28022235" lon="-123.00543652"&gt;…&lt;/trkpt&gt;</pre>
<p>The question I want to answer is simple: <strong>how far did I walk?</strong> The answer to this can't be immediately calculated from the tracks, since the noise makes it look like I ran across the street, crossed back, backed up, jumped forward, <span>&hellip;</span>. I actually walked in mostly-straight lines, as one does. On the other hand, we can't just take the difference between the starting and ending points: I didn't walk a completely straight line either.</p>
<p>For this question, write a Python program <code>calc_distance.py</code> that does the tasks described below. See the included <code>calc_distance_hint.py</code>. Your program must take the path of a <code>.gpx</code> file on the command line, like this:</p>
<pre class="highlight lang-bash">python3 calc_distance.py walk1.gpx</pre>
<h3 id="h-read-the-xml">Read the XML</h3>
<p>Since the input files are XML-based, you'll need to use an XML library to read them. Pick one of  <a href="https://docs.python.org/3/library/xml.dom.minidom.html">xml.dom.minidom</a> (with <a href="https://docs.python.org/3/library/xml.dom.html">xml.dom</a>) or <a href="https://docs.python.org/3/library/xml.etree.elementtree.html">xml.etree.ElementTree</a> (both of which are in the Python standard library). Dealing with XML namespaces in ElementTree can be tricky. Here's a hint:</p>
<pre class="highlight lang-python">parse_result.iter('{http://www.topografix.com/GPX/1/0}trkpt')</pre>
<p>You will need to extract the latitude and longitude from each <code>&lt;trkpt&gt;</code> element. We can ignore the elevation, time, and other fields. <strong>Create a DataFrame</strong> with columns <code>'lat'</code> and <code>'lon'</code> holding the observations. [It's certainly possible to do this without loops, but you may write a loop to iterate as you read the file/elements for this part.]</p>
<h3 id="h-calculate-distances">Calculate Distances</h3>
<p>To get from latitude/longitude points to distances, we'll need some trigonometry: <a href="https://en.wikipedia.org/wiki/Haversine_formula">the haversine formula</a> in particular. You can find more implementation-friendly <a href="http://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206">descriptions of the haversine calculation</a> online, of course. (But remember <a href="AcademicHonesty">AcademicHonesty</a> in your code.)</p>
<p><strong>Write a function</strong> <code>distance</code> that takes a DataFrame as described above, and returns the distance (in metres) between the latitude/longitude points (without any noise reduction: we'll do that next).</p>
<p>This can be done with <a href="http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.shift.html">DataFrame.shift</a> (to get adjacent points into the same rows) and a few expressions on the arrays. If you haven't noticed before, NumPy has implemented <a href="https://docs.scipy.org/doc/numpy/reference/routines.math.html">useful mathematical operations</a> on arrays.</p>
<p>For the record, I get:</p>
<pre class="highlight lang-python">&gt;&gt;&gt; points = pd.DataFrame({
    'lat': [49.28, 49.26, 49.26],
    'lon': [123.00, 123.10, 123.05]})
&gt;&gt;&gt; distance(points)
11217.038892384006</pre>
<p>In your main program, print out the literal distance described in the GPX file, rounded to two decimal places, like this:</p>
<pre class="highlight lang-python">points = read_gpx(sys.argv[1])
print('Unfiltered distance: %0.2f' % (distance(points)))</pre>
<h3 id="h-kalman-filtering">Kalman Filtering</h3>
<p>For the Kalman filter, we need to specify several parameters. The units of measurement in the data are degrees latitude and longitude.</p>
<ul><li>Around Vancouver, one degree of latitude or longitude is about \(10^5\) meters. That will be a close enough conversion as we're estimating error<span>&hellip;</span>
</li><li>While GPS can be accurate to about 5 metres, the reality seems to be several times that: maybe 15 or 20 metres with my phone. (This implies a value for <code>observation_covariance</code>.)
</li><li>Without any other knowledge of what direction I was walking, we must assume that my current position will be the same as my previous position. (<code>transition_matrices</code>)
</li><li>I usually walk something like 1<span>&nbsp;</span>m/s and the data contains an observation about every 10<span>&nbsp;</span>s. (<code>transition_covariance</code>)
</li><li>I have no prior knowledge of where the walk started, but <a href="https://en.wikipedia.org/wiki/Null_Island">the default</a> is probably very far off. The first data point (<code>points.iloc[0]</code>) is probably a much better guess.
</li></ul>
<p>Use these assumptions to create a Kalman filter and reduce the noise in the data. Create a new DataFrame with this data and calculate the <span>&ldquo;</span>true<span>&rdquo;</span> distance I walked.</p>
<p>Print the distance in metres, again to two decimal places. There is no <span>&ldquo;</span>correct<span>&rdquo;</span> answer to give here: closer to reality is better.</p>
<pre class="highlight lang-python">smoothed_points = smooth(points)
print('Filtered distance: %0.2f' % (distance(smoothed_points)))</pre>
<p>Final output should be as in the provided <code>calc_distance.txt</code> (but with a more realistic filtered distance).</p>
<h3 id="h-viewing-your-results">Viewing Your Results</h3>
<p>Once you create the smoothed track in a DataFrame, you can call the provided <code>output_gpx</code> to save it to a file. <strong>Create a GPX file</strong> <code>out.gpx</code> as a side-effect of your program.</p>
<p>A GPX can be viewed online with <a href="http://www.mygpsfiles.com/en/">MyGPSFiles</a>, or with <a href="https://activityworkshop.net/software/gpsprune/download.html">GpsPrune</a> (Ubuntu package <code>gpsprune</code> or download the Java), or in Windows with <a href="http://www.gpstrackeditor.com/">GPS Track Editor</a>. </p>
<p>Have a look at your results: are you smoothing too much or too little? <strong>Tweak the parameters</strong> to your Kalman filter to get the best results you can.</p>
<p>So you can see the kind of results you might expect, I have included a screenshot of a track (but not one of the ones you have) and its smoothed result in MyGPSFiles.</p>
<h2 id="h-questions">Questions</h2>
<p>Answer these questions in a file <code>answers.txt</code>. [Generally, these questions should be answered in a few sentences each.]</p>
<ol><li>When smoothing the CPU temperature, do you think you got a better result with LOESS or Kalman smoothing? What differences did you notice?
</li><li>In the GPX files, you might have also noticed other data about the observations: time stamp, course (heading in degrees from north, 0<span>&ndash;</span>360), speed (in m/s). How could those have been used to make a better prediction about the <span>&ldquo;</span>next<span>&rdquo;</span> latitude and longitude? [Aside: I tried, and it didn't help much. I think the values are calculated from the latitude/longitude by the app: they don't really add much new information.]
</li></ol>
<h2 id="h-submitting">Submitting</h2>
<p>Submit your files through CourSys for <a href="/2018su-cmpt-353-d1/+e3/">Exercise 3</a>.</p></div>

<div class="updateinfo">Updated Mon May 28 2018, 14:06 by ggbaker.

</div>
