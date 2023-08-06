#pragma once

#include <Python.h>

#include "np.hh"
#include "ora.hh"
#include "ora/lib/mem.hh"
#include "py.hh"
#include "py_time.hh"

namespace ora {
namespace py {

using namespace np;

//------------------------------------------------------------------------------

// FIXME: Organize headers better.
template<class TIME> inline std::pair<bool, TIME> maybe_time(Object*);
template<class TIME> inline TIME convert_to_time(Object*);

//------------------------------------------------------------------------------

/*
 * Dispatch for non-ufunc functions to time type-specific implementation.
 */
class TimeAPI
{
private:

  static uint64_t constexpr MAGIC = 0xf17c597caa2e0c48;
  uint64_t const magic_ = MAGIC;

  static TimeAPI*
  get(
    PyArray_Descr* const dtype)
  {
    // Make an attempt to confirm that this is one of our dtypes.
    if (dtype->kind == 'V' && dtype->type == 'j') {
      auto const api = reinterpret_cast<TimeAPI*>(dtype->c_metadata);
      if (api != nullptr && api->magic_ == MAGIC)
        return api;
    }
    return nullptr;
  }

public:

  virtual ~TimeAPI() {}
  virtual ref<Object> from_offset(Array*) = 0;
  virtual LocalDatenumDaytick to_local_datenum_daytick(void const* time_ptr, ora::TimeZone const& tz) const = 0;
  virtual void from_local(Datenum, Daytick, TimeZone const&, bool, void*) const = 0;

  static bool check(PyArray_Descr* const descr)
    { return get(descr) != nullptr; }

  static TimeAPI*
  from(
    PyArray_Descr* const descr)
  {
    auto const api = get(descr);
    if (api == nullptr)
      throw TypeError("not an ora time dtype");
    else
      return api;
  }

};


template<class PYTIME>
class TimeDtype
{
public:

  using Time = typename PYTIME::Time;
  using Offset = typename Time::Offset;

  static void set_up(Module*);
  static Descr* get_descr()
    { return descr_; }

private:

  static Object*        getitem(Time const*, PyArrayObject*);
  static int            setitem(Object*, Time*, PyArrayObject*);
  static int            compare(Time const*, Time const*, PyArrayObject*);

  static void           cast_from_object(Object* const*, Time*, npy_intp, void*, void*);

  static Time add(Time const time, float64_t const seconds)
    { return ora::time::nex::seconds_after(time, seconds); }
  static Time add(float64_t const seconds, Time const time)
    { return ora::time::nex::seconds_after(time, seconds); }
  static Time add(Time const time, int64_t const seconds)
    { return ora::time::nex::seconds_after(time, seconds); }
  static Time add(int64_t const seconds, Time const time)
    { return ora::time::nex::seconds_after(time, seconds); }
  static Time subtract(Time const time, float64_t const seconds)
    { return ora::time::nex::seconds_before(time, seconds); }
  static Time subtract(Time const time, int64_t const seconds)
    { return ora::time::nex::seconds_before(time, seconds); }
  static float64_t subtract(Time const time0, Time const time1)
    { return ora::time::nex::seconds_between(time1, time0); }

  class API
  : public TimeAPI
  {
  public:

    virtual ~API() = default;

    virtual ref<Object> from_offset(Array*) override;

    virtual LocalDatenumDaytick to_local_datenum_daytick(void const* const time_ptr, ora::TimeZone const& tz) const override
      { return ora::nex::to_local_datenum_daytick(*reinterpret_cast<Time const*>(time_ptr), tz); }

    virtual void 
    from_local(
      Datenum const datenum,
      Daytick const daytick,
      TimeZone const& time_zone,
      bool const first,
      void* time_ptr)
      const override
    {
      *reinterpret_cast<Time*>(time_ptr)
        = ora::nex::from_local<Time>(datenum, daytick, time_zone, first);
    }

  };

  static Descr* descr_;

};


template<class PYTIME>
void
TimeDtype<PYTIME>::set_up(
  Module* module)
{
  assert(descr_ == nullptr);
  assert(module != nullptr);

  // Deliberately 'leak' this instance, as it has process lifetime.
  auto arr_funcs = new PyArray_ArrFuncs;
  PyArray_InitArrFuncs(arr_funcs);
  arr_funcs->copyswap   = (PyArray_CopySwapFunc*) generic_copyswap<Time>;
  arr_funcs->copyswapn  = (PyArray_CopySwapNFunc*) generic_copyswapn<Time>;
  arr_funcs->getitem    = (PyArray_GetItemFunc*) getitem;
  arr_funcs->setitem    = (PyArray_SetItemFunc*) setitem;
  arr_funcs->compare    = (PyArray_CompareFunc*) compare;
  // FIMXE: Additional methods.

  descr_ = (Descr*) PyObject_New(PyArray_Descr, &PyArrayDescr_Type);
  descr_->typeobj       = incref(&PYTIME::type_);
  descr_->kind          = 'V';
  descr_->type          = 'j';  // FIXME?
  descr_->byteorder     = '=';
  // FIXME: Requires initialization to INVALID.  Or else Time needs to handle
  // any bit pattern correctly.
  descr_->flags         = 0;
  descr_->type_num      = 0;
  descr_->elsize        = sizeof(Time);
  descr_->alignment     = alignof(Time);
  descr_->subarray      = nullptr;
  descr_->fields        = nullptr;
  descr_->names         = nullptr;
  descr_->f             = arr_funcs;
  descr_->metadata      = nullptr;
  descr_->c_metadata    = (NpyAuxData*) new API();
  descr_->hash          = -1;

  if (PyArray_RegisterDataType(descr_) < 0)
    throw py::Exception();
  int const type_num = descr_->type_num;

  auto const type_dict = (Dict*) PYTIME::type_.tp_dict;

  // Set the dtype as an attribute to the scalar type.
  assert(PYTIME::type_.tp_dict != nullptr);
  type_dict->SetItemString("dtype", (Object*) descr_);

  // Set the offset dtype as an attribute as well.
  auto const offset_type_num = IntType<typename PYTIME::Time::Offset>::type_num;
  // There may be no offset dtype available, e.g. 128-bit integer types.
  if (offset_type_num != -1)
    type_dict->SetItemString(
      "offset_dtype", (Object*) Descr::from(offset_type_num));

  auto const np_module = Module::ImportModule("numpy");

  int constexpr int_type_num = IntType<Offset>::type_num;

  // Cast from object to time.
  Array::RegisterCastFunc(
    NPY_OBJECT, type_num, (PyArray_VectorUnaryFunc*) cast_from_object);
  Array::RegisterCanCast(NPY_OBJECT, type_num, NPY_OBJECT_SCALAR);

  Comparisons<Time, ora::time::nex::equal, ora::time::nex::before>
    ::register_loops(type_num);

  // Arithmetic by seconds.
  create_or_get_ufunc(np_module, "add", 2, 1)->add_loop_2(
    type_num, NPY_FLOAT64, type_num,
    ufunc_loop_2<Time, float64_t, Time, add>);
  create_or_get_ufunc(np_module, "add", 2, 1)->add_loop_2(
    NPY_FLOAT64, type_num, type_num,
    ufunc_loop_2<float64_t, Time, Time, add>);
  create_or_get_ufunc(np_module, "add", 2, 1)->add_loop_2(
    type_num, NPY_INT64, type_num,
    ufunc_loop_2<Time, int64_t, Time, add>);
  create_or_get_ufunc(np_module, "subtract", 2, 1)->add_loop_2(
    type_num, NPY_FLOAT64, type_num,
    ufunc_loop_2<Time, float64_t, Time, subtract>);
  create_or_get_ufunc(np_module, "subtract", 2, 1)->add_loop_2(
    type_num, type_num, NPY_FLOAT64, 
    ufunc_loop_2<Time, Time, float64_t, subtract>);

  // Conversion to offset.
  if (int_type_num != -1) {
    create_or_get_ufunc(module, "to_offset", 1, 1)->add_loop_1(
      type_num, int_type_num,
      ufunc_loop_1<Time, Offset, ora::time::nex::get_offset<Time>>);
  }

  create_or_get_ufunc(module, "is_valid", 1, 1)->add_loop_1(
      type_num, NPY_BOOL,
      ufunc_loop_1<Time, bool, ora::time::nex::is_valid>);
}


template<class PYTIME>
Object*
TimeDtype<PYTIME>::getitem(
  Time const* const data,
  PyArrayObject* const arr)
{
  return PYTIME::create(*data).release();
}


template<class PYTIME>
int
TimeDtype<PYTIME>::setitem(
  Object* const item,
  Time* const data,
  PyArrayObject* const arr)
{
  try {
    *data = convert_to_time<Time>(item);
  }
  catch (Exception) {
    return -1;
  }
  return 0;
}


template<class PYTIME>
int 
TimeDtype<PYTIME>::compare(
  Time const* const t0, 
  Time const* const t1, 
  PyArrayObject* const /* arr */)
{
  return 
      t0->is_invalid() ? -1
    : t1->is_invalid() ?  1
    : t0->is_missing() ? -1
    : t1->is_missing() ?  1
    : *t0 < *t1        ? -1 
    : *t0 > *t1        ?  1 
    : 0;
}


template<class PYTIME>
void
TimeDtype<PYTIME>::cast_from_object(
  Object* const* from,
  Time* to,
  npy_intp num,
  void* /* unused */,
  void* /* unused */)
{
  for (; num > 0; --num, ++from, ++to) {
    auto const time = maybe_time<Time>(*from);
    *to = time.first ? time.second : Time::INVALID;
  }
}


//------------------------------------------------------------------------------
// API implementation

template<class PYTIME>
ref<Object>
TimeDtype<PYTIME>::API::from_offset(
  Array* const offset)
{
  size_t constexpr nargs = 2;
  PyArrayObject* op[nargs] = {(PyArrayObject*) offset, nullptr};
  // Tell the iterator to allocate the output automatically.
  npy_uint32 flags[nargs] 
    = {NPY_ITER_READONLY, NPY_ITER_WRITEONLY | NPY_ITER_ALLOCATE};
  PyArray_Descr* dtypes[nargs] = {Descr::from(NPY_INT64), descr_};

  // Construct the iterator.  We'll handle the inner loop explicitly.
  auto const iter = NpyIter_MultiNew(
    nargs, op, NPY_ITER_EXTERNAL_LOOP, NPY_KEEPORDER, NPY_UNSAFE_CASTING, 
    flags, dtypes);
  if (iter == nullptr)
    throw Exception();

  auto const next = NpyIter_GetIterNext(iter, nullptr);
  auto const inner_stride = NpyIter_GetInnerStrideArray(iter)[0];
  auto const item_size = NpyIter_GetDescrArray(iter)[1]->elsize;

  auto const& inner_size = *NpyIter_GetInnerLoopSizePtr(iter);
  auto const data_ptrs = NpyIter_GetDataPtrArray(iter);

  do {
    // Note: Since dst is newly allocated, it is tightly packed.
    auto src = data_ptrs[0];
    auto dst = data_ptrs[1];
    for (auto size = inner_size; 
         size > 0; 
         --size, src += inner_stride, dst += item_size)
      *reinterpret_cast<Time*>(dst) 
        = ora::time::nex::from_offset<Time>(*reinterpret_cast<int64_t*>(src));
  } while (next(iter));

  // Get the result from the iterator object array.
  auto ret = ref<Array>::of((Array*) NpyIter_GetOperandArray(iter)[1]);
  check_succeed(NpyIter_Deallocate(iter));
  return std::move(ret);
}


//------------------------------------------------------------------------------

template<class PYTIME>
Descr*
TimeDtype<PYTIME>::descr_
  = nullptr;

//------------------------------------------------------------------------------
// Accessories

/*
 * Attempts to convert `arg` to a time array.
 *
 * If it isn't one already, attempts to convert it using the default time dtype.
 */
inline ref<Array>
to_time_array(
  Object* const arg)
{
  if (Array::Check(arg)) {
    // It's an array.  Check its dtype.
    Array* const arr = reinterpret_cast<Array*>(arg);
    if (TimeAPI::check(arr->descr()))
      return ref<Array>::of(arr);
  }

  // Convert to an array of the default time dtype.
  auto const def = TimeDtype<PyTimeDefault>::get_descr();
  return Array::FromAny(arg, def, 0, 0, NPY_ARRAY_BEHAVED);
}


//------------------------------------------------------------------------------

}  // namespace py
}  // namespace ora

