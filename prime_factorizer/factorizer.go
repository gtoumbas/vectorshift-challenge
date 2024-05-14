package main

import (
	"fmt"
	"math/big"
	"math/rand"
	"time"
)

// PollardsRho implements Pollard's Rho algorithm for integer factorization.
func PollardsRho(n *big.Int) *big.Int {
	if n.Cmp(big.NewInt(1)) == 0 {
		return n
	}
	if n.ProbablyPrime(0) {
		return n
	}

	x := big.NewInt(2)
	y := big.NewInt(2)
	d := big.NewInt(1)
	one := big.NewInt(1)
	c := big.NewInt(1)
	g := func(x *big.Int) *big.Int {
		// g(x) = (x^2 + c) % n
		x2 := new(big.Int).Mul(x, x)
		x2.Add(x2, c)
		x2.Mod(x2, n)
		return x2
	}

	for d.Cmp(one) == 0 {
		x = g(x)
		y = g(g(y))
		d.GCD(nil, nil, new(big.Int).Abs(new(big.Int).Sub(x, y)), n)
	}

	if d.Cmp(n) == 0 {
		return PollardsRho(n)
	}

	return d
}

// Returns a slice of prime factors of the given number n.
func PrimeFactors(n *big.Int) []*big.Int {
	var factors []*big.Int

	// Check for number of 2s that divide n
	for new(big.Int).Mod(n, big.NewInt(2)).Cmp(big.NewInt(0)) == 0 {
		factors = append(factors, big.NewInt(2))
		n.Div(n, big.NewInt(2))
	}

	// Use Pollard's Rho to find other factors
	for n.Cmp(big.NewInt(1)) > 0 {
		if n.ProbablyPrime(0) {
			factors = append(factors, new(big.Int).Set(n))
			break
		}

		factor := PollardsRho(n)
		for new(big.Int).Mod(n, factor).Cmp(big.NewInt(0)) == 0 {
			factors = append(factors, new(big.Int).Set(factor))
			n.Div(n, factor)
		}
	}

	return factors
}

func main() {
	rand.Seed(time.Now().UnixNano()) // Seed the random number generator
	n := new(big.Int)
	n.SetString("115792089237316195423570985008687907853269984665640564039457584007913129639937", 10) // Example number
	factors := PrimeFactors(n)
	fmt.Println("Prime factors:")
	for _, factor := range factors {
		fmt.Println(factor)
	}
}