+++
title = "visit struct tag"
author = ["hackrole"]
date = 2021-07-18
lastmod = 2021-07-18T20:21:59+08:00
tags = ["golang"]
draft = false
weight = 2002
+++

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
