#ifndef _FUS_CLASS_H_
#define _FUS_CLASS_H_

/* Simple class system to simplify memory management.
    All instances of a given class have the same size.
    The only class "methods" are init (initialize) and
    cleanup.
    Neither method is allowed to fail, so classes should
    generally support some kind of "zero value" which
    doesn't require any memory allocation, etc.
    It should always be valid to call cleanup on an
    instance which has been initialized.
    Sensible default implementations for these methods
    are fus_class_instance_init_zero and
    fus_class_instance_cleanup_zero.
    These are suitable for e.g. basic integer types. */


#include "core.h"


struct fus_class;
typedef void fus_class_instance_init_t(
    struct fus_class *class,
    void *instance);
typedef void fus_class_instance_cleanup_t(
    struct fus_class *class,
    void *instance);


typedef struct fus_class {
    fus_core_t *core;
    const char *name;
    size_t instance_size;

    /* Instance methods (function pointers and generic data member) */
    void *data;
    fus_class_instance_init_t *instance_init;
    fus_class_instance_cleanup_t *instance_cleanup;

} fus_class_t;



void fus_class_init(
    fus_class_t *class,
    fus_core_t *core,
    const char *name,
    size_t instance_size,
    void *data,
    fus_class_instance_init_t *instance_init,
    fus_class_instance_cleanup_t *instance_cleanup
);

void fus_class_cleanup(fus_class_t *class);


void fus_class_instance_init(fus_class_t *class, void *instance);
void fus_class_instance_cleanup(fus_class_t *class, void *instance);


void fus_class_instance_init_zero(fus_class_t *class, void *instance);
void fus_class_instance_cleanup_zero(fus_class_t *class, void *instance);
void fus_class_init_zero(
    fus_class_t *class,
    fus_core_t *core,
    const char *name,
    size_t instance_size,
    void *data
    /* Just a shorthand for fus_class_init using instance_init_zero
    and instance_cleanup_zero, so you don't have to type them out... */
);


#endif