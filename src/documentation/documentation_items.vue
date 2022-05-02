<script>
/**
 * Below are all items -unordered- inside the Documentation tab.
 * To add an item, use the standard format:

-{
<name> Sometext abcdef </name>
I'm a comment!
Description uses HTML syntax
<description> 
<!-- For code snippets use: -->
<pre>
  <code> p { color: red } </code>
  <code> p { color: blue } </code>
</pre>
</description>
<link> http://www.sometext.abcdef </link>
<other1> sometext abcdef </other1>
Some comment or notes...
<button> sometext abcdef </button>
}-

 *
 * Adding new items -{...}- should be added to documentation_structure.vue to make it visible.
 * 
 * Adding new <tags>, like <button>, should be manually added to Documentation.vue's template.
 * 
 */
export const doctext = 
`
# Documentation items
Item list for in documentation tab

=================================================

-{
<name> FairRecKit </name>
<description> 
WebApp to compare different recommender approaches. Developed by RecCoons, from Utrecht University.
</description>
<link> http://fairreckit.science.uu.nl/ </link>
}-

-----
Tabs:

-{
<name> New Computation </name>
<description>
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
</description>
}-

-{
<name> Active Computations </name>
<description> 
kl
<pre>
  <code> p { color: red } </code>
  <code> p { color: blue } </code>
</pre>
nlmlmloloo
<p>jnl</p>
</description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Documentation </name>
<description> Lorem ipsum dol
or sit amet consectetur adipisicing eli
t. Quae rerum qui

 facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magna
 m quis placeat necessitatibus ea. </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Results </name>
<description> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> All Results </name>
<description> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Datasets </name>
}-

-{
<name> LFM2B </name>
<description> Last FM 2 Billion dataset is a corpus of Music Listening Events for Music Recommendation. It contains more than two billion listening events, intended to be used for various music retrieval and recommendation tasks. </description>
<link> http://www.cp.jku.at/datasets/LFM-2b/ </link>
<other1> sometext </other1>
}-

-{
<name> LFM1B </name>
<description> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> LFM360K </name>
<description> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> ML25M </name>
<description> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> ML100K </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

------

-{
<name> Recommender approaches </name>
}-

-{ 
<name> Elliot </name>
}-

-{
<name> FunkSVD </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> ItemKNN </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> MultiVAE </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> MostPop </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Surprise </name>
}-

-{
<name> PureSVD </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Random </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> SVDpp </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> UserKNN </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Implicit </name>
<description> 
}-

-{
<name> AlternatingLeastSquares </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> BayesianPersonalizedRanking </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> LogisticMatrixFactorization </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Lenskit </name>
}-

-{
<name> BiasedMF </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> ImplicitMF </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> PopScore </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Ra2ndom </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-----

-{
<name> Metrics </name>
}-

-{
<name> P@K </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Rando2m </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> R2andom </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Random2 </name>
<description> sometext </description>
<link> sometext </link>
<other1> sometext </other1>
<button> sometext </button>
}-

-{
<name> Filters </name>
}-

-{
<name> Meta </name>
}-
`
;

</script>
