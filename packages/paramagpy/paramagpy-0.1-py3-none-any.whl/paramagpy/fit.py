import numpy as np
from scipy.optimize import fmin_bfgs
from pprint import pprint

def unique_pairing(a, b):
	"""
	Uniquely map two integers to a single integer.
	The mapped space is minimum size.
	The input is symmetric.

	Parameters
	----------
	a : int
	b : int

	Returns
	-------
	c : int
		unique symmetric mapping (a, b) -> c
	"""
	c = a * b + (abs(a - b) - 1)**2 // 4
	return c

def clean_indices(indices):
	"""
	Uniquely map a list of integers to their smallest size.
	For example: [7,4,7,9,9,10,1] -> [4 2 4 0 0 1 3]

	Parameters
	----------
	indices : array-like integers
		a list of integers

	Returns
	-------
	new_indices : array-like integers
		the mapped integers with smallest size
	"""
	translation = {idx:i for i, idx in enumerate(set(indices))}
	new_indices = [translation[idx] for idx in indices]
	return np.array(new_indices)

def extract_pcs(data):
	"""
	Extract values required for PCS calculations

	Parameters
	----------
	data : list of lists
		A list with elements [Atom, value, error], where Atom is 
		an Atom object, value is the PCS value, and error is the uncertainty

	Returns
	-------
	tuple : (atom coordinates, PCS values, PCS errors, atom indices)
		all information required for PCS calculations
	"""
	atoms, values, errors = zip(*data)
	coords = np.array([i.position for i in atoms])
	values = np.array(values)
	errors = np.array(errors)
	if 0.0 in errors:
		errors = np.ones(len(errors))
		print("Warning: 0.0 value uncertainty. All values weighted evenly")
	idxs = clean_indices([i.serial_number for i in atoms])
	return (coords, values, errors, idxs)

def extract_pre(data):
	"""
	Extract values required for PRE calculations

	Parameters
	----------
	data : list of lists
		A list with elements [Atom, value, error], where Atom is 
		an Atom object, value is the PRE value, and error is the uncertainty

	Returns
	-------
	tuple : (atom coordinates, PRE values, PRE errors, atom indices)
		all information required for PRE calculations
	"""
	atoms, values, errors = zip(*data)
	coords = np.array([i.position for i in atoms])
	gammas = np.array([i.gamma for i in atoms])
	values = np.array(values)
	errors = np.array(errors)
	if 0.0 in errors:
		errors = np.ones(len(errors))
		print("Warning: 0.0 value uncertainty. All values weighted evenly")
	idxs = clean_indices([i.serial_number for i in atoms])
	return (coords, gammas, values, errors, idxs)

def extract_csa(data):
	"""
	Extract CSA tensors from atoms

	Parameters
	----------
	data : list of lists
		A list with elements [Atom, value, error], where Atom is 
		an Atom object, value is the PCS/RDC/PRE value, 
		and error is the uncertainty

	Returns
	-------
	csas : array of 3x3 arrays
		an array of each CSA tensor
	"""
	atoms, values, errors = zip(*data)
	return np.array([i.csa for i in atoms])

def extract_rdc(data):
	"""
	Extract values required for RDC calculations

	Parameters
	----------
	data : list of lists
		A list with elements [Atom, value, error], where Atom is 
		an Atom object, value is the RDC value, and error is the uncertainty

	Returns
	-------
	tuple : (inter-atomic vector, gamma values, RDC values, 
			RDC errors, atom indices)
		all information required for RDC calculations
	"""
	atoms1, atoms2, values, errors = zip(*data)
	vectors = [j.position - i.position for i, j in zip(atoms1, atoms2)]
	gammas = [i.gamma * j.gamma for i, j in zip(atoms1, atoms2)]
	idxs = clean_indices([unique_pairing(i.serial_number, 
		j.serial_number) for i, j in zip(atoms1, atoms2)])
	return map(np.array, [vectors, gammas, values, errors, idxs])

def sphere_grid(origin, radius, points):
	"""
	Make a grid of cartesian points within a sphere

	Parameters
	----------
	origin : float
		the centre of the sphere
	radius : float
		the radius of the sphere
	points : int
		the number of points per radius

	Returns
	-------
	array : array of [x,y,z] coordinates
		the points within the sphere
	"""
	s = np.linspace(-radius, radius, 2*points-1)
	mgrid = np.array(np.meshgrid(s, s, s, indexing='ij')).T.reshape(len(s)**3,3)
	norms = np.linalg.norm(mgrid, axis=1)
	sphere_idx = np.where(norms<=radius)
	return mgrid[sphere_idx] + origin


def svd_calc_metal_from_pcs(pos, pcs, idx):
	"""
	Solve PCS equation by single value decomposition.
	This function is generally called by higher methods like 
	<svd_gridsearch_fit_metal_from_pcs>

	Parameters
	----------
	pos : array of [x,y,z] floats
		the atomic positions in meters
	pcs : array of floats
		the PCS values in ppm
	idx : array of ints
		an index assigned to each atom. Common indices determine summation
		between models for ensemble averaging.

	Returns
	-------
	tuple : (calc, sol)
		calc are the calculated PCS values from the fitted tensor
		sol is the solution to the linearised PCS equation and 
		consists of the tensor matrix elements
	"""
	floatscale = 1E-24
	dist = np.linalg.norm(pos, axis=1)
	x, y, z = pos.T
	a = x**2 - z**2
	b = y**2 - z**2
	c = 2 * x * y
	d = 2 * x * z
	e = 2 * y * z
	mat = (1./(4.*np.pi*dist**5)) * np.array([a,b,c,d,e])
	mat = np.array([np.bincount(idx, weights=col) for col in mat])*1E-24
	matinv = np.linalg.pinv(mat)
	sol = matinv.T.dot(pcs*1E-6)*1E-24
	calc = mat.T.dot(sol)
	return calc, sol


def svd_calc_metal_from_pcs_offset(pos, pcs, idx):
	"""
	Solve PCS equation by single value decomposition with offset.
	An offset arising from referencing errors between diamagnetic
	and paramagnetic datasets can be accounted for using this method.
	This function is generally called by higher methods like 
	<svd_gridsearch_fit_metal_from_pcs>

	NOTE: the factor of 1E26 is required for floating point error mitigation

	Parameters
	----------
	pos : array of [x,y,z] floats
		the atomic positions in meters
	pcs : array of floats
		the PCS values in ppm
	idx : array of ints
		an index assigned to each atom. Common indices determine summation
		between models for ensemble averaging.

	Returns
	-------
	tuple : (calc, sol)
		calc are the calculated PCS values from the fitted tensor
		sol is the solution to the linearised PCS equation and 
		consists of the tensor matrix elements and offset
	"""
	dist = np.linalg.norm(pos, axis=1)
	x, y, z = pos.T
	a = x**2 - z**2
	b = y**2 - z**2
	c = 2 * x * y
	d = 2 * x * z
	e = 2 * y * z
	scale = 1./(4.*np.pi*dist**5)
	mat = scale * np.array([a,b,c,d,e,1E26/scale])
	mat = np.array([np.bincount(idx, weights=col) for col in mat])*1E-24
	matinv = np.linalg.pinv(mat)
	sol = matinv.T.dot(pcs*1E-6)*1E-24
	sol[-1] *= 1E26
	calc = mat.T.dot(sol)
	return calc, sol


def svd_gridsearch_fit_metal_from_pcs(metals, pcss, sumIndices=None,
	origin=None, radius=20.0, points=16, offsetShift=False, progress=None):
	"""
	Fit deltaChi tensor to PCS values using Single Value Decomposition over
	a grid of points in a sphere.

	Parameters
	----------
	metals : list of Metal objects
		a list of metals used as starting points for fitting. 
		a list must always be provided, but may also contain 
		only one element. If multiple metals are provided, each metal
		is fitted to their respective PCS dataset by index, but all are 
		fitted to a common position.
	pcss : list of PCS datasets
		each PCS dataset must correspond to an associated metal for fitting.
		each PCS dataset has structure [Atom, value, error], where Atom is 
		an Atom object, value is the PCS/RDC/PRE value
		and error is the uncertainty
	sumIndices : list of arrays of ints, optional
		each index list must correspond to an associated pcs dataset.
		each index list contains an index assigned to each atom. 
		Common indices determine summation between models 
		for ensemble averaging.
		If None, defaults to atom serial number to determine summation 
		between models.
	origin : float, optional
		the centre of the gridsearch of positions in Angstroms.
		If None, the position of the first metal is used
	radius : float, optional
		the radius of the gridsearch in Angstroms.
	points : int, optional
		the number of points per radius in the gridsearch
	offsetShift : bool, optional
		if True, an offset value added to all PCS values is included in
		the SVD fitting. This may arise due to a referencing error between
		diamagnetic and paramagnetic PCS datasets and may be used when
		many data points are available.
		Default False, no offset is included in the fitting.
	progress : object, optional
		to keep track of the calculation, progress.set(x) is called each
		iteration and varies from 0.0 -> 1.0 when the calculation is complete.

	Returns
	-------
	minmetals : list of metals
		the metals fitted by SVD to the PCS data provided
	"""
	assert len(metals)==len(pcss)

	if origin is None:
		origin = metals[0].position*1E10

	if offsetShift:
		svd_func = svd_calc_metal_from_pcs_offset
	else:
		svd_func = svd_calc_metal_from_pcs

	posarrays = []
	pcsarrays = []
	idxarrays = []
	for pcs in pcss:
		posarray, pcsarray, errarray, idxarray = extract_pcs(pcs)
		posarrays.append(posarray)
		pcsarrays.append(pcsarray)
		idxarrays.append(idxarray)
	sphere = sphere_grid(origin, radius, points)*1E-10

	if sumIndices is not None:
		idxarrays = sumIndices

	tmp = []
	for pcsarray, idxarray in zip(pcsarrays, idxarrays):
		tmp.append(np.bincount(idxarray, weights=pcsarray))
	pcsarrays = tmp

	minscore = 1E50
	print("SVD search started in {} points".format(len(sphere)))
	tot = len(sphere)
	prog = 0.0
	for pos in sphere:
		if progress:
			prog += 1
			progress.set(prog/tot)
		score = 0.0
		for pcsarray, posarray, idxarray in zip(pcsarrays, posarrays, idxarrays):
			coords = posarray - pos
			calculated, solution = svd_func(coords, pcsarray, idxarray)
			score += np.sum((calculated - pcsarray)**2)
		if score<minscore:
			minscore = score
			minpos = pos

	minmetals = [m.copy() for m in metals]
	for pcsarray, posarray, idxarray, metal in zip(pcsarrays, posarrays, 
		idxarrays, minmetals):
		coords = posarray - minpos
		_, solution = svd_func(coords, pcsarray, idxarray)
		metal.position = minpos
		if offsetShift:
			metal.upper_triang = solution[:-1]
			metal.shift = solution[-1]*1E6
		else:
			metal.upper_triang = solution
	return minmetals



def nlr_fit_metal_from_pcs(initMetals, pcss, params, 
	sumIndices=None, userads=False, useracs=False, progress=None):
	"""
	Fit deltaChi tensor to PCS values using non-linear regression.

	Parameters
	----------
	initMetals : list of Metal objects
		a list of metals used as starting points for fitting. 
		a list must always be provided, but may also contain 
		only one element. If multiple metals are provided, each metal
		is fitted to their respective PCS dataset by index, but all are 
		fitted to a common position.
	pcss : list of PCS datasets
		each PCS dataset must correspond to an associated metal for fitting.
		each PCS dataset has structure [Atom, value, error], where Atom is 
		an Atom object, value is the PCS/RDC/PRE value
		and error is the uncertainty
	params : list of str
		the parameters to be fit. 
		For example ['x','y','z','ax','rh','a','b','g','shift']
	sumIndices : list of arrays of ints, optional
		each index list must correspond to an associated pcs dataset.
		each index list contains an index assigned to each atom. 
		Common indices determine summation between models 
		for ensemble averaging.
		If None, defaults to atom serial number to determine summation 
		between models.
	userads : bool, optional
		include residual anisotropic dipolar shielding (RADS) during fitting
	useracs : bool, optional
		include residual anisotropic chemical shielding (RACS) during fitting.
		CSA tensors are taken using the <csa> method of atoms.
	progress : object, optional
		to keep track of the calculation, progress.set(x) is called each
		iteration and varies from 0.0 -> 1.0 when the calculation is complete.

	Returns
	-------
	metals : list of metals
		the metals fitted by NLR to the PCS data provided
	"""
	posarrays = []
	csaarrays = []
	pcsarrays = []
	errarrays = []
	idxarrays = []
	for pcs in pcss:
		posarray, pcsarray, errarray, idxarray = extract_pcs(pcs)
		posarrays.append(posarray)
		pcsarrays.append(pcsarray)
		errarrays.append(errarray)
		idxarrays.append(idxarray)
		if useracs:
			csas = extract_csa(pcs)
			csaarrays.append(csas)
		else:
			csaarrays.append(None)

	metals = [metal.copy() for metal in initMetals]
	pospars = [param for param in params if param in ['x','y','z']]
	otherpars = [param for param in params if param not in ['x','y','z']]

	if sumIndices is not None:
		idxarrays = sumIndices

	def cost(args):
		pos = args[:len(pospars)]
		allother = args[len(pospars):]
		for i, metal in enumerate(metals):
			other = allother[len(otherpars)*i:len(otherpars)*(i+1)]
			metal.set_params(zip(pospars, pos))
			metal.set_params(zip(otherpars, other))
		score = 0.0
		zipped = zip(metals, posarrays, csaarrays, pcsarrays, idxarrays, errarrays)
		for metal, posarray, csaarray, pcsarray, idxarray, errarray in zipped:
			calcpcs = metal.fast_pcs(posarray)
			if userads:
				calcpcs += metal.fast_rads(posarray)
			if useracs:
				calcpcs += metal.fast_racs(csaarray)
			diff = (calcpcs - pcsarray) / errarray
			selectiveSum = np.bincount(idxarray, weights=diff)
			score += np.sum(selectiveSum**2)
		return score

	startpars = metals[0].get_params(pospars)
	for metal in metals:
		pars = metal.get_params(otherpars)
		startpars += pars
	fmin_bfgs(cost, startpars, disp=False)
	for metal in metals:
		metal.set_utr()
	if progress:
		progress.set(1.0)
	return metals


def pcs_fit_error_monte_carlo(initMetals, pcss, params, iterations,
	sumIndices=None, userads=False, useracs=False, progress=None):
	stds = [[] for metal in initMetals]
	atmarrays = []
	pcsarrays = []
	errarrays = []
	for data in pcss:
		atmarray, pcsarray, errarray = zip(*data)
		atmarrays.append(atmarray)
		pcsarrays.append(pcsarray)
		errarrays.append(errarray)

	for i in range(iterations):
		data = []
		for atm, pcs, err in zip(atmarrays, pcsarrays, errarrays):
			noisey = pcs + np.random.normal(scale=err)
			tmp = zip(atm, noisey, err)
			data.append(list(tmp))
		metals = nlr_fit_metal_from_pcs(initMetals, data, params, 
			sumIndices, userads, useracs, progress=None)
		for metal, std in zip(metals, stds):
			std.append(metal.get_params(params))
		if progress:
			progress.set(float(i+1)/iterations)

	return [dict(zip(params, zip(*std))) for std in stds]


def pcs_fit_error_bootstrap(initMetals, pcss, params, iterations, 
	fraction_removed, sumIndices=None, userads=False, useracs=False, 
	progress=None):
	assert 0.0<fraction_removed<1.0
	stds = [[] for metal in initMetals]
	atmarrays = []
	pcsarrays = []
	errarrays = []
	sumarrays = []
	for data in pcss:
		atmarray, pcsarray, errarray = zip(*data)
		atmarrays.append(atmarray)
		pcsarrays.append(pcsarray)
		errarrays.append(errarray)
		sumarrays.append(clean_indices([a.serial_number for a in atmarray]))

	if sumIndices is None:
		sumIndices = sumarrays

	for i in range(iterations):
		datas_trunc = []
		sumIndices_trunc = []
		for atm, pcs, err, idx in zip(atmarrays, pcsarrays, errarrays, sumarrays):
			unique_idx = np.unique(idx)
			chosen_idx = np.random.choice(unique_idx, 
				int(len(unique_idx)*(1-fraction_removed)), replace=False)
			mask = np.isin(idx, chosen_idx)
			idxs_trunc = idx[mask]
			sumIndices_trunc.append(idxs_trunc)
			data_trunc = np.array(list(zip(atm, pcs, err)))[mask]
			datas_trunc.append(data_trunc.tolist())
		metals = nlr_fit_metal_from_pcs(initMetals, datas_trunc, params, 
			sumIndices_trunc, userads, useracs, progress=None)
		for metal, std in zip(metals, stds):
			std.append(metal.get_params(params))
		if progress:
			progress.set(float(i+1)/iterations)

	return [dict(zip(params, zip(*std))) for std in stds]



def fit_metal_from_pcs(metals, pcss):
	fitmetals = svd_gridsearch_calc_metal_from_pcs(metals, pcss)
	fitmetals = nlr_fit_metal_from_pcs(fitmetals, pcss)
	return fitmetals


def plot_pcs_fit(metals, pcss):
	from matplotlib import pyplot as plt
	posarrays = []
	pcsarrays = []
	for pcs in pcss:
		posarray, pcsarray, errarray = extract_pcs(pcs)
		posarrays.append(posarray)
		pcsarrays.append(pcsarray)
	fig = plt.figure(figsize=(5,5))
	ax = fig.add_subplot(111)
	ax.set_xlabel("Experiment")
	ax.set_ylabel("Calculated")
	mini, maxi = min([np.min(i) for i in pcsarrays]), max([np.max(i) for i in pcsarrays])
	ax.plot([mini,maxi], [mini,maxi], '-k', lw=0.5)
	for metal, pos, pcs in zip(metals, posarrays, pcsarrays):
		calc_pcs = metal.fast_pcs(pos)
		ax.plot(pcs, calc_pcs, marker='o', lw=0, ms=3)
	return fig, ax


def qfactor(experiment, calculated, sumIndices=None):
	experiment = np.array(experiment)
	calculated = np.array(calculated)
	if sumIndices is None:
		sumIndices = np.arange(len(experiment))
	diff = experiment - calculated
	numer = np.sum(np.bincount(sumIndices, weights=diff)**2)
	denom = np.sum(np.bincount(sumIndices, weights=experiment)**2)
	return (numer/denom)**0.5


def pcs(metal, atom):
	return metal.pcs(atom.position)



def nlr_fit_metal_from_pre(initMetals, pres, params, sumIndices=None, 
	rtypes=None, usesbm=True, usedsa=True, usecsa=False, progress=None):
	"""
	Fit deltaChi tensor to PCS values using non-linear regression.

	Parameters
	----------
	initMetals : list of Metal objects
		a list of metals used as starting points for fitting. 
		a list must always be provided, but may also contain 
		only one element. If multiple metals are provided, each metal
		is fitted to their respective PCS dataset by index, but all are 
		fitted to a common position.
	pcss : list of PCS datasets
		each PCS dataset must correspond to an associated metal for fitting.
		each PCS dataset has structure [Atom, value, error], where Atom is 
		an Atom object, value is the PCS/RDC/PRE value
		and error is the uncertainty
	params : list of str
		the parameters to be fit. 
		For example ['x','y','z','ax','rh','a','b','g','shift']
	sumIndices : list of arrays of ints, optional
		each index list must correspond to an associated pcs dataset.
		each index list contains an index assigned to each atom. 
		Common indices determine summation between models 
		for ensemble averaging.
		If None, defaults to atom serial number to determine summation 
		between models.
	userads : bool, optional
		include residual anisotropic dipolar shielding (RADS) during fitting
	useracs : bool, optional
		include residual anisotropic chemical shielding (RACS) during fitting.
		CSA tensors are taken using the <csa> method of atoms.
	progress : object, optional
		to keep track of the calculation, progress.set(x) is called each
		iteration and varies from 0.0 -> 1.0 when the calculation is complete.

	Returns
	-------
	metals : list of metals
		the metals fitted by NLR to the PCS data provided
	"""
	if rtypes is None:
		rtypes = ['r2']*len(initMetals)

	posarrays = []
	csaarrays = []
	prearrays = []
	gamarrays = []
	idxarrays = []
	errarrays = []
	for pre in pres:
		posarray, gamarray, prearray, errarray, idxarray = extract_pre(pre)
		posarrays.append(posarray)
		gamarrays.append(gamarray)
		prearrays.append(prearray)
		idxarrays.append(idxarray)
		errarrays.append(errarray)
		if usecsa:
			csas = extract_csa(pre)
			csaarrays.append(csas)
		else:
			csaarrays.append(0.0)

	metals = [metal.copy() for metal in initMetals]
	pospars = [param for param in params if param in ['x','y','z']]
	otherpars = [param for param in params if param not in ['x','y','z']]

	if sumIndices is not None:
		idxarrays = sumIndices

	def cost(args):
		pos = args[:len(pospars)]
		allother = args[len(pospars):]
		for i, metal in enumerate(metals):
			other = allother[len(otherpars)*i:len(otherpars)*(i+1)]
			metal.set_params(zip(pospars, pos))
			metal.set_params(zip(otherpars, other))
		score = 0.0
		zipped = zip(metals, posarrays, gamarrays, csaarrays, 
						prearrays, idxarrays, errarrays, rtypes)
		for metal, posarr, gamarr, csaarr, prearr, idxarr, errarr, rtype in zipped:
			calcpre = metal.fast_pre(posarr, gamarr, rtype, 
				dsa=True, sbm=True, csaarray=csaarr)
			diff = (calcpre - prearr) / errarr
			selectiveSum = np.bincount(idxarr, weights=diff)
			score += np.sum(selectiveSum**2)
		return score

	startpars = metals[0].get_params(pospars)
	for metal in metals:
		pars = metal.get_params(otherpars)
		startpars += pars
	fmin_bfgs(cost, startpars, disp=False)
	for metal in metals:
		metal.set_utr()
	if progress:
		progress.set(1.0)
	return metals


def pre(metal, atom, method='sbm+dsa+csaxdsa', rtype='r2'):
	pos = atom.position
	gam = atom.gamma
	csa = atom.csa()
	rate = 0.0

	methods = method.split('+')
	if 'sbm' in methods and rtype=='r1':
		rate += metal.sbm_r1(pos, gam)
	elif 'sbm' in methods and rtype=='r2':
		rate += metal.sbm_r2(pos, gam)

	if 'dsa' in methods and rtype=='r1':
		rate += metal.curie_r1(pos, gam)
	elif 'dsa' in methods and rtype=='r2':
		rate += metal.curie_r2(pos, gam)

	if 'csa' in methods and rtype=='r1':
		rate += metal.curie_r1(pos, gam, csa=csa, ignorePara=True)
	elif 'csa' in methods and rtype=='r2':
		rate += metal.curie_r2(pos, gam, csa=csa, ignorePara=True)

	if ('csaxdsa' in methods or 'dsaxcsa' in methods) and rtype=='r1':
		pre_dsa = metal.curie_r1(pos, gam)
		pre_csa = metal.curie_r1(pos, gam, csa=csa, ignorePara=True)
		pre_cross = metal.curie_r1(pos, gam, csa=csa)
		rate += pre_cross - pre_dsa - pre_csa
	elif ('csaxdsa' in methods or 'dsaxcsa' in methods) and rtype=='r2':
		pre_dsa = metal.curie_r2(pos, gam)
		pre_csa = metal.curie_r2(pos, gam, csa=csa, ignorePara=True)
		pre_cross = metal.curie_r2(pos, gam, csa=csa)
		rate += pre_cross - pre_dsa - pre_csa

	return rate

def rdc(metal, atom1, atom2):
	vector = (atom1.position - atom2.position)
	return metal.rdc(vector, atom1.gamma, atom2.gamma)
	# vec = (atom1.position - atom2.position)
	# distance = np.linalg.norm(vec)
	# numer = -metal.HBAR * metal.B0**2 * atom1.gamma * atom2.gamma
	# denom = 120. * metal.K * metal.temperature * np.pi**2
	# preFactor = numer/denom
	# p1 = (1./distance**5)*np.kron(vec,vec).reshape(3,3)
	# p2 = (1./distance**3)*np.identity(3)
	# return preFactor * ((3.*p1 - p2).dot(metal.tensor)).trace()

def ccr(metal, atom):
	pass



def svd_calc_metal_from_rdc(vec, rdc_parameterised, idx):
	dist = np.linalg.norm(vec, axis=1)
	x, y, z = vec.T
	a = x**2 - z**2
	b = y**2 - z**2
	c = 2 * x * y
	d = 2 * x * z
	e = 2 * y * z
	mat = (1./dist**5) * np.array([a,b,c,d,e])
	print(idx)
	mat = np.array([np.bincount(idx, weights=col) for col in mat])
	matinv = np.linalg.pinv(mat)
	sol = matinv.T.dot(rdc_parameterised)
	calc = mat.T.dot(sol)
	return calc, sol


def svd_fit_metal_from_rdc(metal, rdc):
	vecarray, gamarray, rdcarray, errarray, idxarray = extract_rdc(rdc)
	pfarray = -3*(metal.MU0 * gamarray * metal.HBAR) / (8 * np.pi**2)
	rdc_param = np.bincount(idxarray, weights=rdcarray / pfarray)
	fitMetal = metal.copy()
	_, sol = svd_calc_metal_from_rdc(vecarray, rdc_param, idxarray)
	fitMetal.upper_triang_saupe = sol
	return fitMetal












