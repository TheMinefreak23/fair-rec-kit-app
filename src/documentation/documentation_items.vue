<script>
/**
 * Below are all items inside the Documentation tab.
 * To add an item, use the standard format:

-{
<name> sometext abcdef </name>
<definition> 
Uses HTML syntax 
For code snippets use:
<pre>
  <code> p { color: red } </code>
  <code> p { color: blue } </code>
</pre>
</definition>
<link> sometext abcdef </link>
<other1> sometext abcdef </other1>
Some comment or notes...
<other_> sometext abcdef </other_>
}-

 * Adding new <tags>, like <other_>, should be manually added to Documentation.vue's template.
 * 
 */
export const doctext = 
`
# Documentation items
Item list for in documentation tab

=================================================

-{
<name> FairRecKit </name>
<definition> 
WebApp to compare different recommender approaches. Developed by RecCoons, from Utrecht University.
</definition>
<link> http://fairreckit.science.uu.nl/ </link>
}-

-----
Tabs:

-{
<name> New Computation </name>
<definition>
<p>In this tab you can start a new computation of your desired datasets and the recommender approach. There are a few well-known datasets built-in, but custom datasets can be uploaded as well. After having chosen the datasets, one or more filters can be applied wat doet dit?.</p>
<p>Next, add the recommender approaches that you want compared and select the number of recommendation per user wat doet dit?. Then, the train-test ratio and the different metrics to compare the performance.</p>
<p>Lastly, enter the metadata to identify your computation. After pressing Send, this data will be added to the queue in Active Computations and send to the server to be executed.</p>
<p>For more information about each step, refer to the list below:</p>
<ul>
<li><a href="#LFM2B">Datasets</li>
<li><a href="#LFM2B">Filters</li>
<li><a href="#FunkSVD">Recommender approaches</li>
<li><a href="###">Train/test-split</li>
<li><a href="tabIndex=1">Metrics</li>
<li><a href="#">Meta</li>
</ul>
</definition>
}-

-{
<name> Active Computations </name>
<definition> 
kl
<pre>
  <code> p { color: red } </code>
  <code> p { color: blue } </code>
</pre>
nlmlmloloo
<p>jnl</p>
</definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> Documentation </name>
<definition> Lorem ipsum dol
or sit amet consectetur adipisicing eli
t. Quae rerum qui

 facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magna
 m quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> Results </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> All results </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-


Datasets:
-{
<name> LFM2B </name>
<definition> Last FM 2 Billion dataset is a corpus of Music Listening Events for Music Recommendation. It contains more than two billion listening events, intended to be used for various music retrieval and recommendation tasks. </definition>
<link> http://www.cp.jku.at/datasets/LFM-2b/ </link>
<other1> sometext </other1>
}-

-{
<name> LFM1B </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> LFM360K </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> ML25M </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> ML100K </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

------

Recommender approaches:

Elliot:
-{
<name> FunkSVD </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> ItemKNN </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> MultiVAE </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> MostPop </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> PureSVD </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> Random </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> SVDpp </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> UserKNN </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

Implicit:
-{
<name> AlternatingLeastSquares </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> BayesianPersonalizedRanking </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> LogisticMatrixFactorization </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

Lenskit:
-{
<name> BiasedMF </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> ImplicitMF </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> PopScore </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> Ra2ndom </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-----

Metrics:
http://www.cp.jku.at/datasets/LFM-2b/

-{
<name> Ran2dom </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> Rando2m </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> R2andom </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

-{
<name> Random2 </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other_> sometext </other_>
}-

`
;

</script>
