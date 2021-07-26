+++
title = "ch11: go测试"
author = ["hackrole"]
date = 2021-07-18
lastmod = 2021-07-26T15:25:51+08:00
tags = ["golang"]
draft = false
weight = 2001
+++

## go test 工具 {#go-test-工具}

file with name endwith \`\_test.go\` was build by \`go test\` instead of \`go build\`

there are three kind of Function need to be remember:

1.  Function which Name starts with \`Test\` was used as UnitTest or FunctionalTest
2.  Function which Name starts with \`Benchmark\` was used as Benmark.
3.  Function which Name starts with 'Example\` was used as Example.


## Test Function {#test-function}

test function must:

1.  import \`testing\` package
2.  has \`t \*testing.T\` as only argument
3.  use tool-function in \`testing.T\` to report fails or logging.

<!--listend-->

```go
package word

// IsPalindrome
func IsPalindrome(s string) bool {
  for i := range s {
    if s[i] != s[len(s)-1-i] {
      return false
    }
  }
  return true
}
```

```go
<<FirstTest>>

<<SecondTest>>

<<ThirdTest>>
```

```go
package word

import "testing"

// TestPalindrome
func TestPalindrome(t *testing.T) {
  if !IsPalindrome("detartrated") {
    t.Errorf(`IsPalindrome("detartrated") = false`)
  }
  if !IsPalindrome("kayak") {
    t.Errorf(`IsPalindrome(kayak) = false`)
  }
}

// TestNonPalindrome
func TestNonPalindrome(t *testing.T) {
  if IsPalindrome("palindrome") {
    t.Errorf(`IsPalindrome("palindrome") = true`)
  }
}
```

```shell
cd ~/projects/learn-by-gopl/ch11 && go test
```

```go
// TestFrencehPalindrome ...
func TestFrencehPalindrome(t *testing.T) {
  if !IsPalindrome("中国中") {
    t.Errorf(`IsPalindrome("中国中") = false`)
  }
}

func TestCanalPalindrome(t *testing.T) {
  input := "A man, a plan, a canal: Panama"
  if !IsPalindrome(input) {
    t.Errorf(`IsPalindrome(%q") = false`, input)
  }
}
```

output detail message with \`-v\` flag

```shell
cd ~/projects/learn-by-gopl/ch11 && go test -v
```

```text
=== RUN   TestPalindrome
--- PASS: TestPalindrome (0.00s)
=== RUN   TestNonPalindrome
--- PASS: TestNonPalindrome (0.00s)
=== RUN   TestFrencehPalindrome
--- FAIL: TestFrencehPalindrome (0.00s)
    word_test.go:26: IsPalindrome("中国中") = false
=== RUN   TestCanalPalindrome
--- FAIL: TestCanalPalindrome (0.00s)
    word_test.go:33: IsPalindrome("A man, a plan, a canal: Panama"") = false
FAIL
exit status 1
FAIL	github.com/hackrole/gopl/ch11	0.001s
```

run certain testcase with \`-run\` flag

```shell
cd ~/projects/learn-by-gopl/ch11 && go test -v -run="French|Canal"
```

```text
=== RUN   TestCanalPalindrome
--- FAIL: TestCanalPalindrome (0.00s)
    word_test.go:33: IsPalindrome("A man, a plan, a canal: Panama"") = false
FAIL
exit status 1
FAIL	github.com/hackrole/gopl/ch11	0.002s
```

```go
package word

import "unicode"

// IsPalindrome
func IsPalindrome(s string) bool {
  var letters []rune
  for _, r := range s {
    if unicode.IsLetter(r) {
      letters = append(letters, unicode.ToLower(r))
    }
  }

  for i := range letters {
    if letters[i] != letters[len(letters)-1-i] {
      return false
    }
  }
  return true
}
```

```shell
cd ~/projects/learn-by-gopl/ch11 && go test -v -run="French|Canal"
```

```text
=== RUN   TestCanalPalindrome
--- PASS: TestCanalPalindrome (0.00s)
PASS
ok  	github.com/hackrole/gopl/ch11	0.001s
```

基于表格的测试方法在go中很常见

```go
// TestPalindrome ...
func TestPalindromeWithTable(t *testing.T)  {
  var tests = []struct{
    input string
    want bool
  }{
    {"", true},
    {"a", true},
    {"aa", true},
    {"ab", false},
    {"kayak", true},
  }

  for _, test := range tests {
    if got := IsPalindrome(test.input); got !=  test.want {
      t.Errorf("IsPalindrome(%q) = %v", test.input, got)
    }
  }

}
```

```shell
cd ~/projects/learn-by-gopl/ch11 && go test
```

```text
PASS
ok  	github.com/hackrole/gopl/ch11	0.001s
```

\`t.Fatal\` and \`t.Fatalf\` used to logging and then stop the testcase,
this must be used in the same goroutine


## test main function {#test-main-function}

```go
package main

import (
  "flag"
  "fmt"
  "io"
  "os"
  "strings"
)

var (
  n = flag.Bool("n", false, "omit trailingnewline")
  s = flag.String("s", " ", "separator")
)

// used for mock
var out io.Writer = os.Stdout

func main() {
  flag.Parse()
  if err := echo(!*n, *s, flag.Args()); err != nil {
    fmt.Fprintf(os.Stdout, "echo: %v\n", err)
    os.Exit(1)
  }
}

// Echo
func Echo(newline bool, sep string, args []string) error {
  fmt.Fprintf(out, strings.Join(args, sep))
  if newline {
    fmt.Fprintf(out)
  }
  return nil
}
```

not call \`log.Fatal\` or \`os.Exit\` in test function.

```go
package main

import (
  "bytes"
  "fmt"
  "testing"
)

// TestEcho ...
func TestEcho(t *testing.T)  {
  var tests = []struct{
    newline bool
    sep string
    args []string
    want string
  }{
    {true, "", []string[], "\n"},
    {false, "", []string{}, ""},
    {true, "\t", []string{"one", "two", "three"}, "one\ttwo\tthree\n"},
    {true, ",", []string{"a", "b", "c"}, "a,b,c\n"}
  }

  for _, test := range tests {
    descr := fmt.Sprintf("echo(%v, %q, %q)", test.newline, test.sep, test.args)
    out = new(bytes.Buffer)
    if err := echo(test.newline, test.sep, test.args); err != nil {
      t.Errorf("%s failed: %v", descr, err)
      continue
    }
    got := out.(*bytes.Buffer).String()
    if got != test.want {
      f.Errorf("%s = %q, want %q", descr, got, test.want)
    }
  }
}
```


## 外部测试包 {#外部测试包}
