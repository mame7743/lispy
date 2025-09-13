(for i 1 15
  (print
    (if (= (% i 15) 0) "FizzBuzz"
        (if (= (% i 3) 0) "Fizz"
            (if (= (% i 5) 0) "Buzz"
                (str i))))))
