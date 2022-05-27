# ALMASim
Generating ALMA simulations for the ML imaging purposes

Instructions:

#### If you have never cloned the repository
1. git clone https://github.com/lukasztychoniec/ALMASim.git
2. cd ALMASim
#### Otherwise
1. cd ALMASim
2. git pull
#### Generate 10 model cubes in the models folder
3. python generate_models.py models params.csv 10

#### Run the sequential simulator and check the printed execution time
4. casa --pipeline --nologger --nologfile --nogui -c "execfile("generate_sims_sequential.py")"
#### Run the parallel simulator and check the printed execution time
5. casa --pipeline --nologger --nologfile --nogui -c "execfile("generate_sims_parallel.py")"

### Bugs
We still don't know how to fid arguments with execfile so, for now, parameters are hardcoded

