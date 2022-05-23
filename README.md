# ALMASim
Generating ALMA simulations for the ML imaging purposes

The pipeline so far was:  
1. Running draw_main.py to generate n images and catalog with info  
2. Running simalma_lines.py to generate .ms files and dirty cubes
3. fix_report.py extracted the info from dirty cubes and created a final catalog  

What we need is a single script to do it all, so perhaps we want a loop that would produce and update catalog entry after each simalma() run.

