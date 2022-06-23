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

This web-app uses the FairRecKit Library to execute all the experiments. A link to the wiki can 
be found <a href=https://github.com/TheMinefreak23/fairreckitlib/wiki>here.
</description>
}-

-----
-{
<name> Documentation </name>
<description>

</description>
}-
-----

-----
-{
<name> How to use </name>
<description>
<ul>
<li> Start a new experiment on <a href="tabIndex=1">New Experiment tab</a>. More information <a href="#New Experiment">below</a>. </li>
<li> Check progress in the <a href="tabIndex=2">Experiment Queue</a>. More information <a href="#Experiment Queue">below</a>.</li>
<li> Get insights into the results in the <a href="tabIndex=3">Results Tab</a>. More information <a href="#Results">below</a>. </li>
<li> See all earlier experiments and edit them on the <a href="tabIndex=4">All Results Tab</a>. More information <a href="#All Results">below</a>.</li>
</ul>

</description>
}-
-----
Tabs:

-{
<name> New Experiment </name>
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

<p>For more information about each step, refer to the list below:</p>
<ul>
<li><a href="#Datasets">Datasets</li>
<li><a href="#Recommender Approaches">Recommender approaches</li>
<li><a href="#Metrics">Metrics</li>
</ul>
</description>
}-

-{
<name> Experiment Queue </name>
<description> 
The experiment queue shows the progress of the current experiment and the queue of experiments that still need to be started or have just started.
This is also the place to go when you want to cancel or abort an experiment in case you do not want it anymore. When an experiment is finished, you can also go to the experiment
result from here.
</description>
}-


-{
<name> Results </name>
<description> This tab shows the results of experiments. New experiment results automatically display here, and you can use the previous results button to the right to open any experiment results.
<p> It shows the title, date and any tags that you added. The filters you applied when before starting the experiment are also displayed. The first table(s) shown on this page display the metrics per run, per dataset. The approach is shown, together with any metrics you selected
when customizing your experiment. You can also copy the experiment settings if you want to run the same experiment again. Another possibility is to validate the experiment. Lastly, you can also export the table with the metric results, so that you can
easily use this for you research. </p>
<h6> Customizability </h6>
<p> Using the checkboxes on the top, you are able to select what you want to be visible in the results. You can choose which datasets show the items per user tables at the bottom. You can also select which
metrics are shown in the tables with the result. </p>

<p> If you look at the tables showing the item per user, you can find two checkboxes above that.
With the first, you can turn the audio snippets on and off, and the second set of checkboxes displays all the tables that are
available and you can select which ones are visible. </p>

<p> If you have a table that shows the recommended or predicted items per user, you are able to customize this table even more. 
First, you can sort the table on any column. Furthermore, you can select any other columns that you want to see in the result. The columns that are available
are dependent on the data that is available in the datasets, such as user or artist gender for music datasets. Another thing that is possible is
to filter the results, so that you can get even more insights into the specific results. </p>
</description>
}-

-{
<name> All Results </name>
<description> The all results tab shows all of the previously executed experiments. From here you can copy settings to start a new experiment.
You can also view the result, which will open it in the results tab. You can edit the name and tags of your experiment and change your email address, for example if you want to validate
that result and have the notification be sent to another address. You can also remove your result if you decide that you will not need it anymore. </description>
}-

-{
<name> Datasets </name>
<description> When you select a dataset, the first thing you choose is the train/testsplit. The standard value for this is 80/20, but you can select any division that you prefer. Next, you select the matrix that you want to use. Then you can choose if you want to apply any filters. These filters are dependent on what information is available in the dataset. 
You can add one or more filters, which creates a subset of the dataset. Then you select the type of split, which can be random or temporal.
or temporal. </description>
}-

-{
<name> LFM2B </name>
<description> Last.fm 2 Billion dataset is a corpus of Music Listening Events for Music Recommendation. It contains more than two billion listening events, intended to be used for various music retrieval and recommendation tasks.
<p> The dataset can be downloaded from <a href="http://www.cp.jku.at/datasets/LFM-2b/">this</a> website.</p>
<p> There are extra optional files that contain extra information, which are all available in the library. All files included in the library are: <i> albums.tsv, artists.tsv, liseting-counts.tsv, listeing-events.tsv, spotify-uris.tsv, tracks.tsv, users.tsv, user_artist_playcound.tsv</i>.
Apart from the required files that contain the listening counts, listening events and user artist playcount, there is also information on things such as album names, artist names, Spotify URI's for Spotify integration, track names, user country, age, gender and creation time. 

</p>   
</description>
}-

-{
<name> LFM1B </name>
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
<name> LFM360K </name>
<description> The Last.fm 360K dataset contains <user, artist, plays> tuples that have been collected from the Last.fm API.
<p> The dataset can be downloaded from <a href="https://www.upf.edu/web/mtg/lastfm360k"> here</a>. The enriched artist gender information can be retrieved from <a href="https://zenodo.org/record/3748787#.YowEBqhByUk">this</a> link. </p>
<p> The following files are handled in the library: <i>usersha1-artmbid-artname-plays.tsv, usersha1-profile.tsv, lfm-360-gender.json </i> </p>

</description>

}-

-{
<name> ML25M </name>
<description> The MovieLens-25M dataset contains 25 million ratings and one million tag applications applied to 62 000 movies by 162 000 users. 
<p> The dataset can be downloaded from <a href="https://grouplens.org/datasets/movielens/25m/">this</a> website.</p>
<p> The following files are handled in the library: <i> genome-scores.csv, genome-tags.csv, links.csv, movies.csv, ratings.csv, tags.csv. </i>
Which means that there is information available on the genome tags and their scores, links to the IMDB-pages, information on the movies and their tags.
</p>
</description>
}-

-{
<name> ML100K </name>
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
<description> A metric is an algorithm which measures the performance/quality of approaches. You can also apply a filter to your metrics. This allows you to customize your
metrics even more.</description>
}-


-{
<name> LensKit Metrics </name>
}-

-{
<name> HR@K </name>
<description> HR@K is an LensKit Accuracy metric. It computes whether of not a list is a hit; any list with at least one relevant item in the first k positions is scored as 0, and lists with no relevant items as 0. Not available for predictions.  </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.hit </link>
}-

-{
<name> NDCG@K </name>
<description> A LensKit Accuracy metric. The NDCG function estimates a utility score for a ranked list of recommendations. Not available for predictions. </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.ndcg </link>
}-

-{
<name> P@K </name>
<description> Compute the recommendation precision. Not available for predictions. </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.precision </link>
}-

-{
<name> R@K </name>
<description> Compute the recommendation recall. Not available for predictions. </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.recall </link>
}-

-{
<name> MRR </name>
<description> Compute the reciprocal rank of the first relevant item in a list of recommendations. Not available for predictions. </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/topn-metrics.html#lenskit.metrics.topn.recip_rank </link>
}-

-{
<name> RMSE </name>
<description> This metric gives the root mean squared approximation error. </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/predict-metrics.html#lenskit.metrics.predict.rmse </link>
}-

-{
<name> MAE </name>
<description> This metric gives the mean absolute approximation error. </description>
<link> https://lkpy.readthedocs.io/en/stable/evaluation/predict-metrics.html#lenskit.metrics.predict.mae </link>
}-

-{
<name> Rexmex </name>
}-

-{
<name> MAPE </name>
<description> Calculates the mean absolute percentage error (MAPE) for a ground-truth prediction vector pair. </description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.rating.mean_absolute_percentage_error </link>
}-

-{
<name> MSE </name>
<description> Calculate the root mean squared error (RMSE) for a ground-truth prediction vector pair. </description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.rating.mean_squared_error </link>
}-

-{
<name> ItemCoverage </name>
<description> It shows the fraction of items which got recommended at least once. Calculates the coverage value for items in possible_user_items given the collcation of recommendations. Recommendation over user/items not in possible_user_items are discarded.  </description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.coverage.item_coverage </link>
}-

-{
<name> UserCoverage </name>
<description> It shows the fraction of users who got at least one recommendation out of all possible users. It calculates the coverage value for users in possible_users_items given the collection of recommendations. Recommendations over users/items not in possible_user_items are discarded. </description>
<link> https://rexmex.readthedocs.io/en/latest/modules/root.html#rexmex.metrics.coverage.user_coverage </link>
}-





`
</script>
