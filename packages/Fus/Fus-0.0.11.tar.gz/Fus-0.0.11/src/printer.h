#ifndef _FUS_PRINTER_H_
#define _FUS_PRINTER_H_


/* * * * * * * * * * * * * * * * * * * * * * * * * * *
 * This file expects to be included by "includes.h"  *
 * * * * * * * * * * * * * * * * * * * * * * * * * * */

#define FUS_PRINTER_BUFSIZE 4096

typedef int fus_printer_flush_t(fus_printer_t *printer);

struct fus_printer {
    int debug; /* Debug level 0, 1, or 2 */

    fus_printer_flush_t *flush; /* callback */
    void *data; /* data for callback, e.g. FILE* */

    char buffer[FUS_PRINTER_BUFSIZE];
    int buffer_len;
    int buffer_maxlen;

    bool shallow_values; /* Don't recurse into arr, obj, fun, etc */
    bool shallow_data; /* Don't recurse into arr */

    int depth;
    const char *tab;
    const char *newline;
};

void fus_printer_init(fus_printer_t *printer);
void fus_printer_cleanup(fus_printer_t *printer);

void fus_printer_set_style_inline(fus_printer_t *printer);
void fus_printer_set_style_full(fus_printer_t *printer);
void fus_printer_set_flush(fus_printer_t *printer,
    fus_printer_flush_t *flush, void *data);
void fus_printer_set_file(fus_printer_t *printer, FILE *file);
int fus_printer_flush_file(fus_printer_t *printer);
int fus_printer_flush(fus_printer_t *printer);

void fus_printer_write(fus_printer_t *printer, const char *text,
    int text_len);
void fus_printer_write_char(fus_printer_t *printer, char c);
void fus_printer_write_text(fus_printer_t *printer, const char *text);
void fus_printer_write_long_int(fus_printer_t *printer, long int i);
void fus_printer_write_tabs(fus_printer_t *printer);
void fus_printer_write_newline(fus_printer_t *printer);


void fus_printer_write_value(fus_printer_t *printer,
    fus_vm_t *vm, fus_value_t value);
void fus_printer_write_boxed(fus_printer_t *printer, fus_boxed_t *p);
void fus_printer_write_arr(fus_printer_t *printer,
    fus_vm_t *vm, fus_arr_t *a);
void fus_printer_write_obj(fus_printer_t *printer,
    fus_vm_t *vm, fus_obj_t *o);
void fus_printer_write_obj_as_data(fus_printer_t *printer,
    fus_vm_t *vm, fus_obj_t *o);
void fus_printer_write_fun(fus_printer_t *printer,
    fus_vm_t *vm, fus_fun_t *f);
void fus_printer_write_data(fus_printer_t *printer,
    fus_vm_t *vm, fus_arr_t *a, int i0, int i1);


#define DEC_FUS_PRINTER_PRINT_T(FNAME, T, TNAME) \
    int fus_printer_print_##FNAME(fus_printer_t *printer, \
        fus_vm_t *vm, fus_##T##_t *TNAME);

DEC_FUS_PRINTER_PRINT_T(arr, arr, a)
DEC_FUS_PRINTER_PRINT_T(obj, obj, o)
DEC_FUS_PRINTER_PRINT_T(obj_as_data, obj, o)
DEC_FUS_PRINTER_PRINT_T(fun, fun, f)
int fus_printer_print_data(fus_printer_t *printer,
    fus_vm_t *vm, fus_arr_t *a, int i0, int i1);
int fus_printer_print_value(fus_printer_t *printer,
    fus_vm_t *vm, fus_value_t value);

#endif