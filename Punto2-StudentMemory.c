#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <inttypes.h>

/* ---------------------------
   Estructuras
   --------------------------- */
typedef struct Student {
    char *first;       /* nombre */
    char *last;        /* apellido */
    unsigned int id:24;/* identificador (24 bits) */
    unsigned int age:7;/* edad (7 bits) */
    size_t n_grades;   /* número de calificaciones */
    double *grades;    /* puntero a array de double */
} Student;

typedef struct {
    Student **items;
    size_t size;
    size_t capacity;
    void *packed_block;      /* bloque contiguo si esta compactado */
    size_t packed_block_size;
} StudentArray;

/* ---------------------------
   Utilidades
   --------------------------- */

/* Alinea hacia arriba 'offset' al múltiplo de 'align' */
static inline size_t align_up(size_t offset, size_t align) {
    size_t m = align - 1;
    return (offset + m) & ~m;
}

/* Pausa y espera que el usuario presione Enter para regresar al menú.
   Además consume cualquier newline pendiente dejado por scanf. */
void pause_return(void) {
    int c;
    /* consumir restos de entrada hasta newline */
    while ((c = getchar()) != '\n' && c != EOF) { /* vacía input */ }
    printf("\nPresiona Enter para regresar al menú...");
    fflush(stdout);
    /* esperar Enter */
    while ((c = getchar()) != '\n' && c != EOF) { /* esperar */ }
    printf("\n");
}

/* Inicialización y liberación general */
void students_init(StudentArray *arr) {
    arr->items = NULL;
    arr->size = 0;
    arr->capacity = 0;
    arr->packed_block = NULL;
    arr->packed_block_size = 0;
}

/* Libera TODO: si está compactado libera el bloque, si no libera asignaciones individuales */
void students_free_all(StudentArray *arr) {
    if (!arr) return;
    if (arr->packed_block) {
        free(arr->packed_block);
        arr->packed_block = NULL;
        arr->packed_block_size = 0;
    } else {
        for (size_t i = 0; i < arr->size; ++i) {
            Student *s = arr->items[i];
            if (!s) continue;
            free(s->first);
            free(s->last);
            free(s->grades);
            free(s);
        }
    }
    free(arr->items);
    arr->items = NULL;
    arr->size = 0;
    arr->capacity = 0;
}

/* Ensure capacity (doubling), no permite cuando está compactado */
int students_ensure_capacity(StudentArray *arr, size_t min_capacity) {
    if (arr->packed_block) {
        fprintf(stderr, "Error: array está compactado. Desempaque antes de modificar.\n");
        return -1;
    }
    if (arr->capacity >= min_capacity) return 0;
    size_t newcap = arr->capacity ? arr->capacity * 2 : 4;
    while (newcap < min_capacity) newcap *= 2;
    Student **tmp = realloc(arr->items, newcap * sizeof(Student*));
    if (!tmp) return -1;
    arr->items = tmp;
    arr->capacity = newcap;
    return 0;
}

/* ---------------------------
   Crear / clonar / liberar estudiante
   --------------------------- */
char *strdup_malloc(const char *s) {
    size_t n = strlen(s) + 1;
    char *p = malloc(n);
    if (!p) return NULL;
    memcpy(p, s, n);
    return p;
}

/* Crea un estudiante con copias de strings y array de notas (las notas se copian) */
Student *student_create(const char *first, const char *last, unsigned int id, unsigned int age,
                        const double *grades, size_t n_grades) {
    if (age > 127 || id >= (1u << 24)) {
        fprintf(stderr, "Valores fuera de rango (age/id).\n");
        return NULL;
    }
    Student *s = malloc(sizeof(Student));
    if (!s) return NULL;
    s->first = strdup_malloc(first ? first : "");
    s->last  = strdup_malloc(last ? last : "");
    s->n_grades = n_grades;
    if (n_grades) {
        s->grades = malloc(n_grades * sizeof(double));
        if (!s->grades) { free(s->first); free(s->last); free(s); return NULL; }
        memcpy(s->grades, grades, n_grades * sizeof(double));
    } else {
        s->grades = NULL;
    }
    s->id = id;
    s->age = age;
    return s;
}

/* Clona un estduainte haciendo una asignacion individual, lo que nos facilita desempaquetar y clonar */
Student *student_clone(const Student *src) {
    if (!src) return NULL;
    return student_create(src->first ? src->first : "",
                          src->last  ? src->last  : "",
                          src->id, src->age,
                          src->grades, src->n_grades);
}

/* ---------------------------
   Añadir estudiante
   - Pregunta por nombre, apellido, id, edad, número de notas y cada nota
   - Crea y añade el estudiante al arreglo (copiando datos)
   --------------------------- */
int students_add(StudentArray *arr, Student *s) {
    if (!arr || !s) return -1;
    if (arr->packed_block) {
        fprintf(stderr, "Error: array está compactado. Desempaque antes de modificar.\n");
        return -1;
    }
    if (students_ensure_capacity(arr, arr->size + 1) != 0) return -1;
    arr->items[arr->size++] = s;
    return 0;
}

int students_add_interactive(StudentArray *arr) {
    char fn[128], ln[128];
    unsigned int id, age;
    int n_grades;
    printf("Nombre: "); if (scanf("%127s", fn) != 1) return -1;
    printf("Apellido: "); if (scanf("%127s", ln) != 1) return -1;
    printf("ID (<=16777215): "); if (scanf("%u", &id) != 1) return -1;
    printf("Edad (<=127): "); if (scanf("%u", &age) != 1) return -1;
    printf("Número de notas (>=0): "); if (scanf("%d", &n_grades) != 1) return -1;
    if (n_grades < 0) n_grades = 0;

    double *grades = NULL;
    if (n_grades > 0) {
        grades = malloc(n_grades * sizeof(double));
        if (!grades) { fprintf(stderr, "Error malloc notas\n"); return -1; }
        for (int i = 0; i < n_grades; ++i) {
            printf("  Nota %d: ", i+1);
            if (scanf("%lf", &grades[i]) != 1) { free(grades); return -1; }
        }
    }

    Student *s = student_create(fn, ln, id, age, grades, (size_t)n_grades);
    free(grades); /* student_create ya hizo copia */
    if (!s) return -1;
    if (students_add(arr, s) != 0) {
        free(s->first); free(s->last); free(s->grades); free(s);
        return -1;
    }
    return 0;
}

/* ---------------------------
   Borrar estudiante (maneja ambos estados)
   - Si el array está compactado, desempaqueta clonando todos excepto el borrado.
   - Si no, libera el estudiante y desplaza el array.
   --------------------------- */
int students_delete(StudentArray *arr, size_t index) {
    if (!arr) return -1;
    if (index >= arr->size) return -1;

    if (arr->packed_block) {
        /* Desempaquetar clonando cada estudiante salvo el index */
        size_t new_count = arr->size - 1;
        Student **new_items = NULL;
        if (new_count > 0) {
            new_items = malloc(new_count * sizeof(Student*));
            if (!new_items) return -1;
        }
        size_t ni = 0;
        for (size_t i = 0; i < arr->size; ++i) {
            if (i == index) continue;
            Student *ps = arr->items[i]; /* apunta dentro del bloque */
            Student *clone = student_clone(ps);
            if (!clone) {
                /* liberar lo ya clonado */
                for (size_t k = 0; k < ni; ++k) {
                    free(new_items[k]->first);
                    free(new_items[k]->last);
                    free(new_items[k]->grades);
                    free(new_items[k]);
                }
                free(new_items);
                return -1;
            }
            new_items[ni++] = clone;
        }
        free(arr->packed_block);
        arr->packed_block = NULL;
        arr->packed_block_size = 0;
        free(arr->items);
        arr->items = new_items;
        arr->size = new_count;
        arr->capacity = new_count > 0 ? new_count : 0;
        return 0;
    } else {
        Student *s = arr->items[index];
        free(s->first);
        free(s->last);
        free(s->grades);
        free(s);
        for (size_t i = index + 1; i < arr->size; ++i) arr->items[i - 1] = arr->items[i];
        arr->size -= 1;
        if (arr->size < arr->capacity / 4 && arr->capacity > 4) {
            size_t newcap = arr->capacity / 2;
            if (newcap < 4) newcap = 4;
            Student **tmp = realloc(arr->items, newcap * sizeof(Student*));
            if (tmp) { arr->items = tmp; arr->capacity = newcap; }
        }
        return 0;
    }
}

/* ---------------------------
   Shrink-to-fit (por estudiante)
   - Ajusta los strings y array de notas al tamaño exacto necesitado.
   - Mostramos estimación antes/después en el menú usando student_memory_estimate.
   --------------------------- */
size_t student_memory_estimate(const Student *s) {
    if (!s) return 0;
    size_t total = 0;
    total += sizeof(Student);
    total += strlen(s->first) + 1;
    total += strlen(s->last) + 1;
    total += s->n_grades * sizeof(double);
    return total;
}

int student_shrink_to_fit(Student *s) {
    if (!s) return -1;
    if (s->first) {
        size_t ln = strlen(s->first) + 1;
        char *nf = realloc(s->first, ln);
        if (nf) s->first = nf;
    }
    if (s->last) {
        size_t ln = strlen(s->last) + 1;
        char *nl = realloc(s->last, ln);
        if (nl) s->last = nl;
    }
    if (s->grades) {
        if (s->n_grades == 0) {
            free(s->grades);
            s->grades = NULL;
        } else {
            double *ng = realloc(s->grades, s->n_grades * sizeof(double));
            if (ng) s->grades = ng;
        }
    }
    return 0;
}

/* ---------------------------
   Compactar todo
   - Reserva un único bloque que contiene structs + strings + arrays contiguos.
   - Actualiza arr->items para apuntar dentro del bloque.
   - Hay que tener en cuenta que mientras esté compactado no se deben free() individualmente.
   --------------------------- */
int students_compact_all(StudentArray *arr) {
    if (!arr) return -1;
    if (arr->packed_block) { fprintf(stderr, "Array ya está compactado.\n"); return 0; }

    size_t total = 0;
    size_t align_double = sizeof(double) > (size_t)_Alignof(Student) ? sizeof(double) : (size_t)_Alignof(Student);
    for (size_t i = 0; i < arr->size; ++i) {
        Student *s = arr->items[i];
        total = align_up(total, (size_t)_Alignof(Student));
        total += sizeof(Student);
        total += strlen(s->first) + 1;
        total += strlen(s->last) + 1;
        total = align_up(total, align_double);
        total += s->n_grades * sizeof(double);
    }
    if (total == 0) return 0;
    void *block = malloc(total);
    if (!block) return -1;
    char *cursor = (char*)block;
    size_t used = 0;
    Student **new_items = malloc(arr->size * sizeof(Student*));
    if (!new_items) { free(block); return -1; }

    for (size_t i = 0; i < arr->size; ++i) {
        Student *old = arr->items[i];
        size_t off_struct = align_up(used, (size_t)_Alignof(Student));
        Student *dest = (Student*)((char*)block + off_struct);
        used = off_struct + sizeof(Student);

        size_t off_first = used;
        char *dest_first = (char*)block + off_first;
        size_t len_first = strlen(old->first) + 1;
        memcpy(dest_first, old->first, len_first);
        used = off_first + len_first;

        size_t off_last = used;
        char *dest_last = (char*)block + off_last;
        size_t len_last = strlen(old->last) + 1;
        memcpy(dest_last, old->last, len_last);
        used = off_last + len_last;

        size_t off_grades = align_up(used, align_double);
        double *dest_grades = (double*)((char*)block + off_grades);
        if (old->n_grades > 0) memcpy(dest_grades, old->grades, old->n_grades * sizeof(double));
        used = off_grades + old->n_grades * sizeof(double);

        dest->first = dest_first;
        dest->last  = dest_last;
        dest->id = old->id;
        dest->age = old->age;
        dest->n_grades = old->n_grades;
        dest->grades = dest_grades;

        new_items[i] = dest;
    }

    /* liberar individuales */
    for (size_t i = 0; i < arr->size; ++i) {
        Student *old = arr->items[i];
        free(old->first);
        free(old->last);
        free(old->grades);
        free(old);
    }
    free(arr->items);

    arr->items = new_items;
    arr->packed_block = block;
    arr->packed_block_size = used;
    arr->capacity = arr->size;
    return 0;
}

/* ---------------------------
   Desempaquetar todo
   - Convierte el bloque compacto (arr->packed_block) en asignaciones individuales.
   - Esto permite modificar (añadir/borrar) con normalidad tras compactar.
   - Complejidad: O(n) tiempo y O(n) memoria temporal para las nuevas asignaciones.
   --------------------------- */
int students_unpack_all(StudentArray *arr) {
    if (!arr) return -1;
    if (!arr->packed_block) {
        /* ya desempaquetado */
        return 0;
    }
    size_t n = arr->size;
    Student **new_items = malloc(n * sizeof(Student*));
    if (!new_items) return -1;
    for (size_t i = 0; i < n; ++i) {
        Student *ps = arr->items[i]; /* apuntan dentro del bloque */
        /* clonamos cada estudiante a asignaciones individuales */
        Student *clone = student_clone(ps);
        if (!clone) {
            /* libera lo creado */
            for (size_t k = 0; k < i; ++k) {
                free(new_items[k]->first);
                free(new_items[k]->last);
                free(new_items[k]->grades);
                free(new_items[k]);
            }
            free(new_items);
            return -1;
        }
        new_items[i] = clone;
    }
    /* liberar bloque compacto y sustituir los elmnetos */
    free(arr->packed_block);
    arr->packed_block = NULL;
    arr->packed_block_size = 0;
    arr->items = new_items;
    /* ajustar capacidad: al menos 4 para comportamiento estable */
    arr->capacity = n > 4 ? n : 4;
    return 0;
}

/* ---------------------------
   Estadísticas / impresión
   --------------------------- */
void students_list(const StudentArray *arr) {
    if (!arr) return;
    printf("Total estudiantes: %zu%s\n", arr->size, arr->packed_block ? " (compactado)" : "");
    for (size_t i = 0; i < arr->size; ++i) {
        Student *s = arr->items[i];
        printf("[%zu] %s %s | ID: %u | Age: %u | #Notas: %zu\n",
               i, s->first, s->last, s->id, s->age, s->n_grades);
        if (s->n_grades > 0) {
            printf("     Notas: ");
            for (size_t j = 0; j < s->n_grades; ++j) {
                printf("%.2f", s->grades[j]);
                if (j + 1 < s->n_grades) printf(", ");
            }
            printf("\n");
        }
    }
}

/* Estimación total (suma de los pedidos de memoria; pero no incluye metadata del asignador) */
uint64_t students_memory_usage(const StudentArray *arr) {
    if (!arr) return 0;
    uint64_t total = 0;
    if (arr->packed_block) total += (uint64_t)arr->packed_block_size;
    else {
        for (size_t i = 0; i < arr->size; ++i) {
            Student *s = arr->items[i];
            total += sizeof(Student);
            total += (uint64_t)(strlen(s->first) + 1);
            total += (uint64_t)(strlen(s->last) + 1);
            total += (uint64_t)(s->n_grades * sizeof(double));
        }
    }
    total += (uint64_t)(arr->capacity * sizeof(Student*));
    return total;
}

/* Desglose por estudiante */
void print_memory_breakdown(const StudentArray *arr) {
    printf("== Desglose por estudiante ==\n");
    for (size_t i = 0; i < arr->size; ++i) {
        Student *s = arr->items[i];
        size_t est = student_memory_estimate(s);
        printf(" [%zu] %s %s : ~%zu bytes\n", i, s->first, s->last, est);
    }
    uint64_t total = students_memory_usage(arr);
    printf(" Estimación total: %" PRIu64 " bytes (incluye array de punteros)\n", total);
}

/* ---------------------------
   Interfaz (menu) y main
   --------------------------- */
void print_menu(void) {
    puts("\n--- Gestor de Estudiantes (Optimizacion dw memoriaa) ---");
    puts("1) Listar estudiantes");
    puts("2) Añadir estudiante");
    puts("3) Borrar estudiante por índice");
    puts("4) Shrink-to-fit (por índice)");
    puts("5) Compactar todo (pack en bloque contiguo)");
    puts("6) Mostrar uso estimado de memoria");
    puts("7) Desempaquetar todo (unpack)");
    puts("8) Salir");
    printf("Elija opción: ");
}

int main(void) {
    StudentArray arr;
    students_init(&arr);

    /* Estudiantes para ejemplo inicial */
    double g1[] = {4.5, 3.7, 4.0};
    double g2[] = {3.8, 3.9};
    double g3[] = {4.0, 4.2, 3.6, 4.1};
    students_add(&arr, student_create("María", "Rodríguez", 1001, 21, g1, 3));
    students_add(&arr, student_create("Valentina", "Gómez",    1002, 20, g2, 2));
    students_add(&arr, student_create("Juan",   "Pérez",      1003, 22, g3, 4));

    int opt = 0;
    while (1) {
        print_menu();
        if (scanf("%d", &opt) != 1) { int c; while ((c=getchar())!='\n' && c!=EOF); continue; }

        if (opt == 1) {
            students_list(&arr);
            pause_return();
        } else if (opt == 2) {
            if (arr.packed_block) {
                printf("Advertencia: array compactado. Desempaque antes de añadir.\n");
            } else {
                if (students_add_interactive(&arr) == 0) printf("Añadido correctamente.\n");
                else printf("Error al añadir.\n");
            }
            pause_return();
        } else if (opt == 3) {
            size_t idx; printf("Índice a borrar: ");
            if (scanf("%zu", &idx) != 1) { int c; while ((c=getchar())!=EOF && c!='\n'); pause_return(); continue; }
            if (students_delete(&arr, idx) == 0) printf("Eliminado.\n");
            else printf("Índice inválido o error.\n");
            pause_return();
        } else if (opt == 4) {
            size_t idx; printf("Índice a shrink-to-fit: ");
            if (scanf("%zu", &idx) != 1) { int c; while ((c=getchar())!=EOF && c!='\n'); pause_return(); continue; }
            if (idx >= arr.size) { printf("Índice inválido.\n"); pause_return(); continue; }
            if (arr.packed_block) {
                printf("Advertencia: array compactado. Desempaque antes de shrink-to-fit.\n");
                pause_return();
                continue;
            }
            Student *s = arr.items[idx];
            size_t before = student_memory_estimate(s);
            printf("Antes (estimado): %zu bytes\n", before);
            student_shrink_to_fit(s);
            size_t after = student_memory_estimate(s);
            printf("Después (estimado): %zu bytes\n", after);
            printf("Ahorro estimado: %zu bytes\n", before > after ? before - after : 0);
            pause_return();
        } else if (opt == 5) {
            if (students_compact_all(&arr) == 0) printf("Compactación completada. Bytes usados: %zu\n", arr.packed_block_size);
            else printf("Error al compactar.\n");
            pause_return();
        } else if (opt == 6) {
            print_memory_breakdown(&arr);
            pause_return();
        } else if (opt == 7) {
            if (arr.packed_block) {
                if (students_unpack_all(&arr) == 0) printf("Desempaquetado completado. Ahora puede modificar normalmente.\n");
                else printf("Error al desempaquetar.\n");
            } else {
                printf("El array ya está desempaquetado (no hay bloque compacto).\n");
            }
            pause_return();
        } else if (opt == 8) {
            break;
        } else {
            printf("Opción no válida.\n");
            pause_return();
        }
    }

    students_free_all(&arr);
    printf("Saliendo. Recursos liberados.\n");
    return 0;
}


