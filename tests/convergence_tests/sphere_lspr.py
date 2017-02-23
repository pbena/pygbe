from pygbe.util import an_solution
from convergence_lspr import (mesh_ratio, run_convergence, picklesave, pickleload,
                              report_results, mesh)

def main():
    print('{:-^60}'.format('Running sphere_lspr test'))
    try:
        test_outputs = pickleload()
    except FileNotFoundError:
        test_outputs = {}

    problem_folder = 'input_files'

    # dirichlet_surface
    param = 'sphere_complex.param'
    test_name = 'sphere_complex'
    if test_name not in test_outputs.keys():
       N, iterations, expected_rate, Cext_0, Time = run_convergence(
            mesh, test_name, problem_folder, param)
       test_outputs[test_name] = {'N': N, 'iterations': iterations,
                                  'expected_rate': expected_rate, 'Cext_0': Cext_0,
                                  'Time': Time} 
    picklesave(test_outputs)

    # load data for analysis
    N = test_outputs[test_name]['N']
    iterations = test_outputs[test_name]['iterations']
    expected_rate = test_outputs[test_name]['expected_rate']
    Cext_0 = test_outputs[test_name]['Cext_0']
    Time = test_outputs[test_name]['Time']

    total_time = Time
    
    #This test is for 10 nm radius silver sphere in water, at wavelength 380 nm 
    radius = 10.
    wavelength = 380.
    diel_out = 1.7972083599999999 + 1j * 8.504766399999999e-09 #water value extrapolated
    diel_in = -3.3876520488233184 + 1j * 0.19220746083441781 #silver value extrapolated

    analytical = an_solution.Cext_analytical(radius, wavelength, diel_out, diel_in)

    error = abs(Cext_0 - analytical) / abs(analytical)

    test_outputs[test_name]['error'] = error
    test_outputs[test_name]['analytical'] = analytical
 
    report_results(error,
                   N,
                   expected_rate,
                   iterations,
                   Cext_0,
                   analytical,
                   total_time,
                   test_name='sphere_complex')


if __name__ == "__main__":
    main()
