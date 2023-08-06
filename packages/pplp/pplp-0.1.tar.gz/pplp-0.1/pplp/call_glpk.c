#include <glpk.h>
#include <time.h>
#include <stdio.h>

double call_glpk(long vars, double *objective, double *value, long dir,
		 long var_bound_len, 
		 long *var_bound, double *var_lower, double *var_upper,
		 long auxvar_bound_len, 
		 long *auxvar_bound, double *auxvar_lower, double *auxvar_upper,
		 long amatrix_elements,
		 int *amatrix_i, int *amatrix_j, double *amatrix_r,
		 long var_kind_len, long *var_kind, int use_simplex,
		 int verbose) {
  long i;
  if (verbose) glp_term_out(GLP_ON);
  else glp_term_out(GLP_OFF);

  glp_prob *lp = glp_create_prob();
  int is_mip = 0;
  glp_set_obj_dir(lp, dir);

  glp_add_cols(lp, vars);
  for (i=1; i<=vars; i++) {
    glp_set_obj_coef(lp, i, objective[i]);
    if (i<var_bound_len && var_bound[i]>0)
      glp_set_col_bnds(lp, i, var_bound[i], var_lower[i], var_upper[i]);
    if (i<var_kind_len && var_kind[i]>0) {
      glp_set_col_kind(lp, i, var_kind[i]);
      if (var_kind[i] != GLP_CV) is_mip=1;
    }
  }

  if (auxvar_bound_len > 0) {
    glp_add_rows(lp, auxvar_bound_len-1);
    for (i=1; i<auxvar_bound_len; i++) {
      glp_set_row_bnds(lp, i, auxvar_bound[i], auxvar_lower[i], auxvar_upper[i]);
    }
  }

  if (amatrix_elements-1 > 0) {
    glp_load_matrix(lp, amatrix_elements-1, amatrix_i, amatrix_j, amatrix_r);
  }

  double z;
//  clock_t t0 = clock();
  if (use_simplex) {
      glp_smcp params;
      glp_init_smcp(&params);
      params.presolve = GLP_ON;
      glp_simplex(lp, &params);
      z = glp_get_obj_val(lp);
  } else {
      int e = glp_interior(lp, NULL);
      if (e) printf("glp_interior failed: %d\n", e);
      z = glp_ipt_obj_val(lp); // Not working :(
  }
//  clock_t t1 = clock();
//  printf("IN %f s\n", ((float)(t1-t0))/((float)CLOCKS_PER_SEC));

  if (is_mip) {
    glp_intopt(lp, NULL);
    z = glp_mip_obj_val(lp);
  }

  for (i=1; i<=vars; i++) {
    if (i<var_kind_len && var_kind[i]>0 && var_kind[i]!=GLP_CV) {
      value[i] = glp_mip_col_val(lp, i);
    } else {
      value[i] = glp_get_col_prim(lp, i);
    }
  }

  glp_delete_prob(lp);
  return z;
}
