# ALMASim
Generating ALMA simulations for the ML imaging purposes

Instructions:

1 Create a conda environment:
<pre><code>conda create --name casa6.5 python=3.8 </code><pre>
2 Activate it:
<pre><code>conda activate casa6.5</code></pre>
3 Move to the folder where you want to store the results
4 Clone the GitHub repository:
<pre><code>git clone https://github.com/lukasztychoniec/ALMASim.git</pre></code>
5 Make sure that the required libraries are installed, we are supposing to be on a centos system:
<pre><code>
    sudo yum install ImageMagick*
    sudo yum install xorg-x11-server-Xvfb
    sudo yum install compat-libgfortran-48
    sudo yum install libnsl
    sudo yum install openmpi-devel
    sudo yum install mpich-devel
</pre><code>
6 Install the required python libraries
<pre><code>pip install -r requirements.txt</code></pre>
7 Generate the sky model cubes:
<pre><code>python generate_models.py models params.csv n </code></pre>
where the first parameter is the path of the directory in which to store the sky <b>models</b>, <b>params.csv</b> is the name of the .csv file which holds the sources parameters and <b>n</b> is the number of cubes to generate
8 Generate the ALMA simulations:
<pre><code>python generate_sims.py models sims </code></pre>
where <b>models</b> is the path to the directory where the sky models where generated, and <b>sims</b> is the path to the directory where you want to store the simulations.
9 Now that the simulations are concluded, we neet to update the parameters in the <b>params.csv</b> file. To do so run the following command
<pre><code>python generate_parameters.py models sims </code></pre>

