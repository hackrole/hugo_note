+++
title = "ch12: 反射reflection"
author = ["hackrole"]
date = 2021-07-18
lastmod = 2021-07-18T20:26:51+08:00
tags = ["golang"]
draft = false
weight = 2001
+++

## introduce {#introduce}

在编译是不知道类型的情况下，可在运行时查看值，调用方法，更新变量，以及对布局进行操作的机制.

反射让我们把类型当作头等值

动态类型 vs 动态值

反射定义了两个重要的类型 reflect.Type, reflect.Value


### reflect.Type 类型描述符 {#reflect-dot-type-类型描述符}

接口值的动态类型也是类型描述符

满足fmt.Stringer接口

```go
t := reflect.TypeOf(3)
fmt.Println(t.String())
fmt.Println(t)

// 反射总是返回具体类型
var w io.Writer = os.Stdout
fmt.Println(reflect.TypeOf(w)) // return os.File
```

```text
int
int
*os.File
```


### reflect.Value {#reflect-dot-value}

```go
v := reflect.ValueOf(3)
fmt.Println(v)
// this will handle  reflect.Value
fmt.Println("%v\n", v)
// implement the fmt.Stringer interface, but only return `Type` if not string
fmt.Println(v.String())

// get `Value` Type
t := v.Type()
fmt.Println(t.String())

// the reverse operator
x := v.Interface() // return `interface{}`
i := x.(int) // type cast
fmt.Printf("%d\n", i)
```

```text
3
%v
 3
<int Value>
int
3
```


#### vs interface{}. {#vs-interface-dot}

interface{}隐藏布局信息和内置操作，除非知道动态类型，不然无法完成操作.
Value包含可以用来分析值的信息


#### Kind {#kind}

Bool, String, <number> Array, Strut, Chan, Func, Ptr, Slice, Map, Inteface, Invalid

```go
package main

import (
  "fmt"
  "reflect"
  "strconv"
  "time"
)

// Any: format Any value to string
func Any(value interface{}) string {
  return formatAtom(reflect.ValueOf(value))
}

// formatATom ...
func formatAtom(v reflect.Value) string {
  switch v.Kind() {
  case reflect.Invalid:
    return "invalid"
  case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
    return strconv.FormatInt(v.Int(), 10)
  case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
    return strconv.FormatUint(v.Uint(), 10)
  case reflect.Bool:
    return strconv.FormatBool(v.Bool())
  case reflect.String:
    return strconv.Quote(v.String())
  case reflect.Chan, reflect.Func, reflect.Ptr, reflect.Slice, reflect.Map:
    return v.Type().String() + " 0x" + strconv.FormatUint(uint64(v.Pointer()), 16)
  default:
    return v.Type().String() + " value"
  }
}

func main() {
  var x int64 = 1
  var d time.Duration = 1 * time.Nanosecond
  fmt.Println(Any(x))
  fmt.Println(Any(d))
  fmt.Println(Any([]int64{x}))
  fmt.Println(Any([]time.Duration{d}))
}
```

```text
1
1
[]int64 0xc00001c160
[]time.Duration 0xc00001c168
```


#### Display {#display}

TODO eval??

```go
import "eval"
import "fmt"

// main ...
func main()  {
  e, _ := eval.Parse("sqrt(A / pi)")
  fmt.Println(e)
}
```

```go
package main

import (
  "fmt"
  "os"
  "reflect"
  "strconv"
)

// Display
func Display(name string, x interface{}) {
  fmt.Printf("Display %s (%T):\n", name, x)
  display(name, reflect.ValueOf(x))
}

func formatAtom(v reflect.Value) string {
  switch v.Kind() {
  case reflect.Invalid:
    return "invalid"
  case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
    return strconv.FormatInt(v.Int(), 10)
  case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
    return strconv.FormatUint(v.Uint(), 10)
  case reflect.Bool:
    return strconv.FormatBool(v.Bool())
  case reflect.String:
    return strconv.Quote(v.String())
  case reflect.Chan, reflect.Func, reflect.Ptr, reflect.Slice, reflect.Map:
    return v.Type().String() + " 0x" + strconv.FormatUint(uint64(v.Pointer()), 16)
  default:
    return v.Type().String() + " value"
  }
}

// display
func display(path string, v reflect.Value) {
  switch v.Kind() {
  case reflect.Invalid:
    fmt.Printf("%s = invalid\n", path)
  case reflect.Slice, reflect.Array:
    for i := 0; i < v.Len(); i++ {
      display(fmt.Sprintf("%s[%d]", path, i), v.Index(i))
    }
  case reflect.Struct:
    for i := 0; i < v.NumField(); i++ {
      fieldPath := fmt.Sprintf("%s.%s", path, v.Type().Field(i).Name)
      display(fieldPath, v.Field(i))
    }
  case reflect.Map:
    for _, key := range v.MapKeys() {
      display(fmt.Sprintf("%s[%s]", path, formatAtom(key)), v.MapIndex(key))
    }
  case reflect.Ptr:
    if v.IsNil() {
      fmt.Printf("%s = nil\n", path)
    } else {
      display(fmt.Sprintf("(*%s)", path), v.Elem())
    }
  case reflect.Interface:
    if v.IsNil() {
      fmt.Printf("%s = nil\n", path)
    } else {
      fmt.Printf("%s.type = %s\n", path, v.Elem().Type())
      display(path+".value", v.Elem())
    }
  default:
    fmt.Printf("%s = %s\n", path, formatAtom(v))
  }

}

type Movie struct {
  Title, Subtitle string
  Year            int
  Color           bool
  Actor           map[string]string
  Oscars          []string
  Sequel          *string
}

func main() {
  strangelove := Movie{
    Title:    "Dr.StrangeLove",
    Subtitle: "How I learned to Stop worrying and Love the Bomb",
    Year:     1964,
    Color:    false,
    Actor: map[string]string{
      "Dr. Strangelove":            "peter sellers",
      "Grp. Capt. Lionel Mandrake": "Peter Sellers",
      "Pres. Merkin Muffley":       "Peter Sellers",
      "Gen. Buck Turgidson":        "George C. Scott",
    },
    Oscars: []string{
      "Best Actor (Nomin.)",
      "Best Adapted Screenpaly (Nomin.)",
    },
  }
  Display("strangelove", strangelove)

  // display os.File
  Display("os.Stderr", os.Stderr)

  // display reflect.Vlaue
  Display("rv", reflect.ValueOf(os.Stderr))

  // diff
  var i interface{} = 3
  Display("i", i)
  Display("&i", &i)
}
```

```text
Display strangelove (main.Movie):
strangelove.Title = "Dr.StrangeLove"
strangelove.Subtitle = "How I learned to Stop worrying and Love the Bomb"
strangelove.Year = 1964
strangelove.Color = false
strangelove.Actor["Dr. Strangelove"] = "peter sellers"
strangelove.Actor["Grp. Capt. Lionel Mandrake"] = "Peter Sellers"
strangelove.Actor["Pres. Merkin Muffley"] = "Peter Sellers"
strangelove.Actor["Gen. Buck Turgidson"] = "George C. Scott"
strangelove.Oscars[0] = "Best Actor (Nomin.)"
strangelove.Oscars[1] = "Best Adapted Screenpaly (Nomin.)"
strangelove.Sequel = nil
Display os.Stderr (*os.File):
(*(*os.Stderr).file).pfd.fdmu.state = 0
(*(*os.Stderr).file).pfd.fdmu.rsema = 0
(*(*os.Stderr).file).pfd.fdmu.wsema = 0
(*(*os.Stderr).file).pfd.Sysfd = 2
(*(*os.Stderr).file).pfd.pd.runtimeCtx = 0
(*(*os.Stderr).file).pfd.iovecs = nil
(*(*os.Stderr).file).pfd.csema = 0
(*(*os.Stderr).file).pfd.isBlocking = 1
(*(*os.Stderr).file).pfd.IsStream = true
(*(*os.Stderr).file).pfd.ZeroReadIsEOF = true
(*(*os.Stderr).file).pfd.isFile = true
(*(*os.Stderr).file).name = "/dev/stderr"
(*(*os.Stderr).file).dirinfo = nil
(*(*os.Stderr).file).nonblock = false
(*(*os.Stderr).file).stdoutOrErr = true
(*(*os.Stderr).file).appendMode = false
Display rv (reflect.Value):
(*rv.typ).size = 8
(*rv.typ).ptrdata = 8
(*rv.typ).hash = 871609668
(*rv.typ).tflag = 1
(*rv.typ).align = 8
(*rv.typ).fieldAlign = 8
(*rv.typ).kind = 54
(*(*rv.typ).alg).hash = func(unsafe.Pointer, uintptr) uintptr 0x453580
(*(*rv.typ).alg).equal = func(unsafe.Pointer, unsafe.Pointer) bool 0x402d80
(*(*rv.typ).gcdata) = 1
(*rv.typ).str = 8406
(*rv.typ).ptrToThis = 0
rv.ptr = unsafe.Pointer value
rv.flag = 22
Display i (int):
i = 3
Display &i (*interface {}):
(*&i).type = int
(*&i).value = 3
```


### 使用reflect.Value设置值 {#使用reflect-dot-value设置值}


#### 可寻址 {#可寻址}

```go
x := 2
// ValueOf都是不可寻址
a := reflect.ValueOf(2) // no
b := reflect.ValueOf(x) // no
c := reflect.ValueOf(&x) // no
d := c.Elem() // yes

fmt.Println(a.CanAddr())
fmt.Println(b.CanAddr())
fmt.Println(c.CanAddr())
fmt.Println(d.CanAddr())
```

```text
false
false
false
true
```


#### 设置值 {#设置值}

```go
x := 2
d := reflect.ValueOf(&x).Elem()
// method 1
px := d.Addr().Interface().(*int)
*px = 3
fmt.Println(x)

// method 2
d.Set(reflect.ValueOf(4))
fmt.Println(x)
////  below crash
// d.SEt(reflect.ValueOf(int64(5))) // type error
// d := reflect.ValueOf(3)
// d.Set(reflect.ValueOf(3)) // 不可寻址

// useage method
d = reflect.ValueOf(&x).Elem()
d.SetInt(3)
fmt.Println(x)


// canset

stdout := reflect.ValueOf(os.Stdout).Elem()
fmt.Println(stdout.Type())
fd := stdout.FieldByName("fd")
// fmt.Println(fd.Int())
// // fd.SetInt(2) // this raise, case not export-variable cannot be set
fmt.Println(fd.CanAddr(), fd.CanSet())
```

```text
3
4
3
os.File
false false
```


## <span class="org-todo todo TODO">TODO</span> encode S-expression {#encode-s-expression}


## visit struct tag {#visit-struct-tag}

```go
package main

import (
  "fmt"
  "http"
  "reflect"
)

// search ...
func search(resp http.ResponseWriter, req *http.Request) {
  var data struct {
    Labels     []string `http:"1"`
    MaxResults int      `http:"max"`
    Exact      bool     `http:"x"`
  }
  data.MaxResults = 10
  if err := Unpack(req, &data); err != nil {
    http.Error(resp, err.Error(), http.StatusBadRequest)
    return
  }

  fmt.Fprintf(resp, "Search: %+v\n", data)
}

// Unpack
func Unpack(req *http.Request, ptr interface{}) error {
  if err := req.ParseForm(); err != nil {
    return err
  }

  fields := make(map[string]reflect.Value)
  v := reflect.VaueOf(ptr).Elem()
  for i := 0; i < v.NumField(); i++ {
    fieldInfo := v.Type().Field(i)
    tag := fieldInfo.Tag
    name := tag.get("http")
    if name == "" {
      name = strings.ToLower(fieldInfo.Name)
    }
    fields[name] = v.Field(i)
  }

  for name, vaues := range req.Form {
    f := fields[name]
    if !f.IsValid() {
      continue
    }
    for _, value := range values {
      if f.Kind() == reflect.Slice {
        elem := reflect.New(f.Type().Elem()).Elem()
        if err := populate(elem, value); err != nil {
          return fmt.Errorf("%s: %v", name, err)
        }
        f.Set(reflect.Append(f, elem))
      } else {
        if err := populate(f, value); err != nil {
          return fmt.Errorf("%s: %v", name, err)
        }
      }
    }
  }
  return nil
}

// Populate
func Populate(v reflect.value, value string) error {
  //swtich...
}
```


## <span class="org-todo todo TODO">TODO</span> display type and call method. {#display-type-and-call-method-dot}

```go
// Print
func Print(x interface{})  {
  v := reflect.ValueOf(x)
  t := v.Type()
  fmt.Println("type %s\n", t)

  for i := 0; i < v.NumMethod(); i++ {
    methType := v.Method(i).Type()
    fmt.Prinf("func (%s) %s%s\n", t, t.Method(i).Name, strings.TrimPrefix(methType.String(), "func")
  }

}
```


## 注意事项 {#注意事项}

谨慎使用:

1.  基于反射的代码很脆弱, 编译时变成运行时
2.  无法很好的文档化
3.  性能会慢一到二个数量级
