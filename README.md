# ALMASim
Generating ALMA simulations for the ML imaging purposes

Instructions:

1 Create a conda environment:
<pre><code>conda create --name casa6.5 python=3.8 </code></pre>
2 Activate it:
<pre><code>conda activate casa6.5</code></pre>
3 Move to the folder where you want to store the results
4 Clone the GitHub repository:
<pre><code>git clone https://github.com/lukasztychoniec/ALMASim.git</pre></code>
5 Make sure that the required libraries are installed, we are supposing to be on a centos system:

<pre><code>sudo yum install ImageMagick*</code></pre>
<pre><code>sudo yum install xorg-x11-server-Xvfb</code></pre>
<pre><code>sudo yum install compat-libgfortran-48</code></pre>
<pre><code>sudo yum install libnsl</code></pre>
<pre><code>sudo yum install openmpi-devel</code></pre>
<pre><code>sudo yum install mpich-devel</code></pre>
<pre><code>sudo yum install parallel</code></pre>

6 Install the required python libraries
<pre><code>pip install -r requirements.txt</code></pre>
7 Generate the sky model cubes:
<pre><code>python generate_models.py models sims params.csv n </code></pre>
where the first parameter <b>models</b> is the name of the directory in which to store the <b>sky models</b> cubes, the second <b>sims</b> is the name of the directory in which to store the simulations, the third <b>params.csv</b> is the name of the .csv file which holds the sources parameters and the fourth <b>n</b> is the number of cubes to generate
8 Generate the ALMA simulations:
In order to generate the simulations, we are going to run the <b>alma_simulator.py</b> script in parallel with GNU Parall.
First, after running the generate_models.py script, you can see that script not only populated the models directory with the sky models .fits files, but also created the <b>sim_parameters.txt</b> text file.
This file can be used in combination with the <b>generate_sims.sh</b> bash script to generate the simulations in parallel using all available cores. To do so type the following:
<pre><code>parallel  --eta --colsep ' ' -a sims_parameters.txt  sh generate_sims.sh </code></pre>
The script assumes that you have used all the default parameter name outlined in this README and that the conda environment is called conda6.5. If this is not the case, modity the generate_sims.sh script accordingly.
9 Now that the simulations are concluded, we neet to update the parameters in the <b>params.csv</b> file with the fluxes and continuum values. To do so run the following command:
<pre><code>python generate_parameters.py models sims </code></pre>
10 You are all ready to train and test your models. 
