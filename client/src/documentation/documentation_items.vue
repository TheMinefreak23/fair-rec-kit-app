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
export const doctext = `
# Documentation items
Item list for in documentation tab

=================================================

-{
<name> FairRecKit </name>
<description> 
The FairRecKit is a web-based analysis software that aids in understanding the underlying
mechanisms of recommender systems. It includes:
<ul>
<li> 5 datasets </li>
<li> 11 metrics </li>
<li> 20 algorithms </li>
</ul> 

On this page you can find the information on how to use it per tab, and information on the datasets, metrics and algorithms that are used. 

<p>This web-app uses the <b>FairRecKit Library</b> to execute all the experiments. A link to the FairRecKitLib wiki can 
be found <a href=https://github.com/TheMinefreak23/fairreckitlib/wiki>here</a>.</p>
</description>
}-


-{
<name> How to use </name>
<description>
The FairRecKit can be used to analyse different recommender approaches and datasets, using different metrics. You can run an experiment with different settings, you can see the progress and then 
view the result. 

 <p> There are three ways you can run an experiment:
  <ul>
  <li>Start a new experiment</li>
  <li>Validate a finished experiment</li>
  <li>Copy settings from a finished experiment</li>
  </ul>

  <p> The basic way to run an experiment is by starting a <b>new experiment</b>. This can be done in the <i>New Experiment tab</i> , which is explained further down below. You select all the settings that you 
  want and then <i>send</i> the experiment to the server to be run.  
  </p>

  <p> In case you want to <b>validate</b> a finished experiment, you go to the result of the experiment, which can be done through the <i>All Results tab</i>. You go to view the result, which opens it on the
  <i>Result tab</i>. Here, you have the option on the top right to fill in how many times you would like the experiment to be run again and then press the button <i> validate run</i>.</p>

  <p> The last option is to <b>copy settings</b> from a finished experiment. Just as validation, you first need to make sure you have the result you want to copy open in the <i> Result tab</i>. Then you select the <i>copy settings</i> button, which
  will take you to the <i>New Experiment tab</i> but it will have all the settings that you applied already filled in, so you can just change what you want to have differently.</p>
  
  </p>

<b> What are the tabs? </b>
<ul>
<li> Start a new experiment on <a href="tabIndex=1">New Experiment tab</a>. </li>
<li> Check progress in the <a href="tabIndex=2">Experiment Queue</a>. </li>
<li> Get insights into the results in the <a href="tabIndex=3">Results Tab</a>. </li>
<li> See all earlier experiments and edit them on the <a href="tabIndex=4">All Results Tab</a>. </li>
</ul>

</description>
}-
-----
Tabs:

-{
<name> New Experiment Tab </name>
<description>

<p> You can start out with selecting whether the experiment type should be <b>recommendation or prediction</b>.
Predictions are predicted ratings for known user-item pairs in the data , while recommendations are a list of recommended items for a user based on these predicted ratings.
</p>
<p> Next, you can give <b>metadata</b> such as the name for the experiment, any tags that you want to add and your email address.
If you add your email address, you will receive an email once the experiment has finished. </p>
<p> After that, you can select your <b>dataset(s)</b>. More specific information on the datasets can be found <a href="#Datasets"> below</a>. 
For each dataset you add, you can give the train/testsplit, type of split, select the matrix you want to be used in the experiment and optionally add any filters.
</p>
<p> You can also add one or more <b>recommender algorithms</b>. For more information about all the specific approaches, see <a href="#Recommender Approaches">below</a>. 
You can also select the number of recommendations per user and choose if you want to include already rated items in recommendations. This is only possible for recommendation algorithms, not for prediction algorithms.</p>
<p> The final step is to select <b>metrics</b>. For more information on the metrics, see <a href="#Metrics">below</a>. You can add one or more metrics. For each metric you can define the necessary parameters and an optional filter.</p>

</description>
}-

-{
<name> Experiment Queue Tab </name>
<description> 
The experiment queue <b>shows the progress</b> of the current experiment and the queue of experiments that still need to be started or have just started.
This is also the place to go when you want to <b>cancel or abort</b> an experiment in case you do not want it anymore. When an experiment is finished, you can also go to the experiment
result from here.
</description>
}-


-{
<name> Results Tab </name>
<description> This tab <b>shows the results of an experiment</b>. New experiment results automatically display here, and you can use the previous results button to the right to open any experiment results.
<p> On this tab you can:
<ul>
<li> View a specific result </li>
<li> Copy settings </li>
<li> Validate experiment </li>
</ul>
</p>

<h5> Viewing a specific result </h5>
<p> When viewing a specific result the title, date and any tags that you added are shown. The filters you applied when before starting the experiment are also displayed. The result <b>metrics</b> are displayed in the first few tables on the page, they are 
shown per run, per dataset. Below the Metrics header, the <b> user-item results</b> are shown in table form. </p>

<p> You can <b>customize your view</b>. You can select which datasets are showing the items per user, you can select which user/item tables show and select if snippets are shown. You can also sort the tables and for the user/item tables, you can change the pagination.
<ul>
<li> For selecting which datasets are showing items per user you can use checkboxes under the "Datasets showing items per user:" and select the datasets. </li>
<li> To turn on snippets you can select or deselect the checkbox that says "show snippets".</li>
<li> To select which user/item tables are shown you can select the checkboxes under "select items to be shown:". </li>
<li> For sorting tables, you can click on the header that you want it to be sorted on.</li>
</ul>
<p> Lastly, you can also <b>export your result</b>. For this, you can use the "export" button that appears under the table that shows the metrics.</p>

<h5> Copy settings </h5>
For copying settings of the experiment, you go to the top and press the <i> copy settings </i> button. This shows all the settings that you had for that experiment, and if you confirm, you will go
to the New Experiment tab, but with all these settings pre filled.

<h5> Validate experiment </h5>
For validating an experiment, you go to the top right. Here you see a field where you can fill in the number of runs. Press the <i>validate run</i> button to add the validation experiments to the queue.

</description>
}-

-{
<name> All Results Tab </name>
<description> The all results tab shows all of the previously executed experiments. From here you can copy settings to start a new experiment.
You can also view the result, which will open it in the results tab. You can edit the name and tags of your experiment and change your email address, for example if you want to validate
that result and have the notification be sent to another address. You can also remove your result if you decide that you will not need it anymore. </description>
}-

-{
<name> Datasets </name>
<description> When you select a dataset, the first thing you choose is the train/testsplit. The standard value for this is 80/20, but you can select any division that you prefer. Next, you select the matrix that you want to use. Then you can choose if you want to apply any filters. These filters are dependent on what information is available in the dataset. 
You can add one or more filters, which creates a subset of the dataset. Then you select the type of split, which can be random or temporal. </description>
}-

-{
<name> LFM-2B </name>
<description> Last.fm 2 Billion dataset is a corpus of Music Listening Events for Music Recommendation. It contains more than two billion listening events, intended to be used for various music retrieval and recommendation tasks.
<p> The dataset can be downloaded from <a href="http://www.cp.jku.at/datasets/LFM-2b/">this</a> website.</p>
<p> There are extra optional files that contain extra information, which are all available in the library. All files included in the library are: <i> albums.tsv, artists.tsv, liseting-counts.tsv, listeing-events.tsv, spotify-uris.tsv, tracks.tsv, users.tsv, user_artist_playcound.tsv</i>.
Apart from the required files that contain the listening counts, listening events and user artist playcount, there is also information on things such as album names, artist names, Spotify URI's for Spotify integration, track names, user country, age, gender and creation time. 

</p>   
</description>
}-

-{
<name> LFM-1B </name>
<description> 
The Last.fm 1 Billion dataset is a corpus of Music Listening Events for Music Recommendation. It has more than one billion listening events.
<p> The dataset and user genre profile can be found on <a href="http://www.cp.jku.at/datasets/LFM-1b/">this</a> website. The enriched artist gender information can be retrieved <a href=" https://zenodo.org/record/3748787#.YowEBqhByUk">here</a>.</p>
<p> The following files are included in the FairRecKitLib <i> LFM-1b_albums.txt,
    LFM-1b_artist_genres_allmusic.txt,
    LFM-1b_artists.txt,
    LFM-1b_LEs.mat,
    LFM-1b_LEs.txt,
    LFM-1b_tracks.txt,
    LFM-1b_UGP_noPC_allmusic.txt,
    LFM-1b_UGP_weightedPC_allmusic.txt,
    LFM-1b_users.txt,
    LFM-1b_users_additional.txt,
    lfm-gender.json</i>
    
  Which means that apart from the listening events, there is also information on the albums, genres, artist, tracks, additional user info and user genre profiles. There is also information
  on the gender of the artists. </p>
</description>
}-

-{
<name> LFM-360K </name>
<description> The Last.fm 360K dataset contains <user, artist, plays> tuples that have been collected from the Last.fm API.
<p> The dataset can be downloaded from <a href="https://www.upf.edu/web/mtg/lastfm360k"> here</a>. The enriched artist gender information can be retrieved from <a href="https://zenodo.org/record/3748787#.YowEBqhByUk">this</a> link. </p>
<p> The following files are handled in the library: <i>usersha1-artmbid-artname-plays.tsv, usersha1-profile.tsv, lfm-360-gender.json </i> </p>

</description>

}-

-{
<name> ML-25M </name>
<description> The MovieLens-25M dataset contains 25 million ratings and one million tag applications applied to 62 000 movies by 162 000 users. 
<p> The dataset can be downloaded from <a href="https://grouplens.org/datasets/movielens/25m/">this</a> website.</p>
<p> The following files are handled in the library: <i> genome-scores.csv, genome-tags.csv, links.csv, movies.csv, ratings.csv, tags.csv. </i>
Which means that there is information available on the genome tags and their scores, links to the IMDB-pages, information on the movies and their tags.
</p>
</description>
}-

-{
<name> ML-100K </name>
<description> The MovieLens-100K dataset contains 100 000 ratings from 1000 users on 1700 movies. 
<p> The dataset can be found on <a href="https://grouplens.org/datasets/movielens/100k/">this</a> website. </p>
<p> The library handles the following files <i>u.data, u.user, u.item</i>. 
This means that the dataset contains information on the ratings but also simple demographic info for the users (age, gender, occupation, zip).
</p>
</description>
}-

------

-{
<name> Recommender approaches </name>
<description> <p>The recommender approaches that are implemented in the library come from LensKit, Implicit and Surprise. Below, these algorithms are categorized and there is a link to the documentation
from the libraries that they come from.</p>

<p><b>Matrix Factorization Algorithms:</b></p>
<ul> 
<li> BiasedMF (<a href="https://lkpy.readthedocs.io/en/stable/mf.html#lenskit.algorithms.als.BiasedMF">LensKit</a>)</li>
<li> ImplicitMF (<a href="https://lkpy.readthedocs.io/en/stable/mf.html#lenskit.algorithms.als.ImplicitMF">LensKit</a>)</li>
<li> AlternatingLeastSquares (<a href="https://implicit.readthedocs.io/en/latest/als.html">Implicit</a>)</li>
<li> BayesianPersonalizedRanking (<a href="https://implicit.readthedocs.io/en/latest/bpr.html">Implicit</a>)</li>
<li> LogisticMatrixFactorization (<a href="https://implicit.readthedocs.io/en/latest/lmf.html">Implicit</a>)</li>
<li> BaselineOnlyALS (<a href="">Surprise</a>)</li>
<li> BaselineOnlySGD (<a href="">Surprise</a>)</li>
<li> SVD (<a href="">Surprise</a>)</li>
<li> SVDpp (<a href="">Surprise</a>)</li>
<li> NMF (<a href="">Surprise</a>)</li>
</ul>

<p><b>Collaborative Filtering Algorithms:</b></p> 
<ul> 
<li> ItemItem (<a href="https://lkpy.readthedocs.io/en/stable/knn.html#lenskit.algorithms.item_knn.ItemItem">LensKit</a>) </li>
<li> UserUser (<a href="https://lkpy.readthedocs.io/en/stable/knn.html#lenskit.algorithms.user_knn.UserUser">LensKit</a>) </li>
<li> KNNBasic (<a href="https://surprise.readthedocs.io/en/stable/knn_inspired.html#surprise.prediction_algorithms.knns.KNNBasic">Surprise</a>)</li>
<li> KNNBaselineALS (<a href="https://surprise.readthedocs.io/en/stable/basic_algorithms.html?highlight=baselineonly#surprise.prediction_algorithms.baseline_only.BaselineOnly">Surprise</a>)</li>
<li> KNNBaselineSGD (<a href="https://surprise.readthedocs.io/en/stable/knn_inspired.html#surprise.prediction_algorithms.knns.KNNBaseline">Surprise</a>)</li>
<li> KNNWithMeans (<a href="https://surprise.readthedocs.io/en/stable/knn_inspired.html#surprise.prediction_algorithms.knns.KNNWithMeans">Surprise</a>)</li>
<li> KNNWithZScore (<a href="https://surprise.readthedocs.io/en/stable/knn_inspired.html#surprise.prediction_algorithms.knns.KNNWithZScore">Surprise</a>)</li>
<li> CoClustering (<a href="https://surprise.readthedocs.io/en/stable/co_clustering.html#surprise.prediction_algorithms.co_clustering.CoClustering">Surprise</a>)</li>
<li> SlopeOne (<a href="https://surprise.readthedocs.io/en/stable/slope_one.html#surprise.prediction_algorithms.slope_one.SlopeOne">Surprise</a>)</li>
</ul>

<p><b>Basic and Utility Algorithms:</b></p>
<ul>
<li> PopScore (<a href="https://lkpy.readthedocs.io/en/stable/basic.html?highlight=popscore#lenskit.algorithms.basic.PopScore">LensKit</a>)</li>
<li> Random (<a href="https://lkpy.readthedocs.io/en/stable/basic.html?highlight=popscore#lenskit.algorithms.basic.Random">LensKit</a>)</li>
</ul>

</description>
}-


-----

-{
<name> Metrics </name>
<description> <p> A metric is an algorithm which measures the performance/quality of approaches. You can also apply a filter to your metrics. This allows you to customize your
metrics even more. For the metrics, implementations from <a href="https://lkpy.readthedocs.io/en/stable/">LensKit</a> and <a href="https://rexmex.readthedocs.io/en/latest/index.html">Rexmex</a> have been used. The following metrics are available: </p>
<b>Accuracy: </b>
<ul>
<li> HR@K (LensKit) </li>
<li> NDCG@K (LensKit) </li>
<li> P@K (LensKit) </li>
<li> R@K (LensKit)</li>
<li> MRR (LensKit)</li>
</ul>

<b> Coverage: </b>
<ul>
<li> Item Coverage (Rexmex)</li>
<li> User Coverage (Rexmex)</li>
</ul>

<b> Rating: </b>
<ul>
<li> MAE (LensKit)</li>
<li> MAPE (Rexmex)</li>
<li> MSE (Rexmex)</li>
<li> RMSE (LensKit)</li>
</ul>



</description>
}-


-{
<name> LensKit Metrics </name>
}-


-{
<name> HR@K </name>
<description> HR@K is an LensKit Accuracy metric. It computes whether of not a list is a hit; any list with at least one relevant item in the first k positions is scored as 0, and lists with no relevant items as 0. Not available for predictions.  
Documentation can be found <a href="https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.hit">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.hit </link>
}-

-{
<name> NDCG@K </name>
<description> A LensKit Accuracy metric. The NDCG function estimates a utility score for a ranked list of recommendations. Not available for predictions. 
Documentation can be found <a href="https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.ndcg">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.ndcg </link>
}-

-{
<name> P@K </name>
<description> Compute the recommendation precision. Not available for predictions. 
Documentation can be found <a href="https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.precision">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.precision </link>
}-

-{
<name> R@K </name>
<description> Compute the recommendation recall. Not available for predictions. 
Documentation can be found <a href="https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.recall">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.recall </link>
}-

-{
<name> MRR </name>
<description> Compute the reciprocal rank of the first relevant item in a list of recommendations. Not available for predictions. 
Documentation can be found <a href="">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.recip_rank </link>
}-

-{
<name> RMSE </name>
<description> This metric gives the root mean squared approximation error. 
Documentation can be found <a href="">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/predict-metrics.html#lenskit.metrics.predict.rmse </link>
}-

-{
<name> MAE </name>
<description> This metric gives the mean absolute approximation error. 
Documentation can be found <a href="">here</a>.
</description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/predict-metrics.html#lenskit.metrics.predict.mae </link>
}-

-{
<name> Rexmex </name>
}-

-{
<name> MAPE </name>
<description> Calculates the mean absolute percentage error (MAPE) for a ground-truth prediction vector pair. 
Documentation can be found <a href="">here</a>.
</description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.rating.mean_absolute_percentage_error </link>
}-

-{
<name> MSE </name>
<description> Calculate the root mean squared error (RMSE) for a ground-truth prediction vector pair. 
Documentation can be found <a href="">here</a>.
</description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.rating.mean_squared_error </link>
}-

-{
<name> ItemCoverage </name>
<description> It shows the fraction of items which got recommended at least once. Calculates the coverage value for items in possible_user_items given the collcation of recommendations. Recommendation over user/items not in possible_user_items are discarded.  
Documentation can be found <a href="">here</a>.
</description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.coverage.item_coverage </link>
}-

-{
<name> UserCoverage </name>
<description> It shows the fraction of users who got at least one recommendation out of all possible users. It calculates the coverage value for users in possible_users_items given the collection of recommendations. Recommendations over users/items not in possible_user_items are discarded. 
Documentation can be found <a href="">here</a>.
</description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.coverage.user_coverage </link>
}-





`
</script>
