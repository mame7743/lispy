;; 関数型FizzBuzz
(let ((fizzbuzz_check (lambda (n)
                        (if (= (% n 15) 0)
                            "FizzBuzz"
                            (if (= (% n 3) 0)
                                "Fizz"
                                (if (= (% n 5) 0)
                                    "Buzz"
                                    (str n)))))))
  (for i 1 15 (print (fizzbuzz_check i))))
