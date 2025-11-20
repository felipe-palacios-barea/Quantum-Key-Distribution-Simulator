
import random
from typing import List, Tuple

# Configuration
BASIS_RECTILINEAR = '+'
BASIS_DIAGONAL = 'x'
AVAILABLE_BASES = [BASIS_RECTILINEAR, BASIS_DIAGONAL]

class BB84ProtocolSimulation:
    """
    A simulation of the BB84 Quantum Key Distribution protocol.
    This class manages the actors (Alice, Bob, Eve) and the stages of the protocol.
    """

    def __init__(self, num_bits: int = 50):
        self.num_bits = num_bits

    def _generate_random_bits(self, n: int) -> List[int]:
        """Helper: Generates a list of n random bits (0s and 1s)."""
        return [random.randint(0, 1) for _ in range(n)]

    def _generate_random_bases(self, n: int) -> List[str]:
        """Helper: Generates a list of n random bases (+ or x)."""
        return [random.choice(AVAILABLE_BASES) for _ in range(n)]

    def _measure_photon(self, original_bit: int, original_basis: str, measurement_basis: str) -> int:
        """
        Simulates the physics of measuring a photon.
        
        Logic:
        1. If we measure in the SAME basis it was sent in, we get the exact bit back (Deterministic).
        2. If we measure in a DIFFERENT basis, the result is random (Probabilistic).
        """
        if original_basis == measurement_basis:
            return original_bit
        else:
            return random.randint(0, 1)

    def run(self, with_eavesdropper: bool = False):
        print(f"\n{'='*60}")
        print(f"Starting Simulation: {'WITH EAVESDROPPER (EVE)' if with_eavesdropper else 'SECURE CHANNEL'}")
        print(f"{'='*60}")

        #Step 1: Alice Prepares the Photons
        alice_bits = self._generate_random_bits(self.num_bits)
        alice_bases = self._generate_random_bases(self.num_bits)
        
        print(f"1. Alice prepares {self.num_bits} qubits.")
        print(f"   Sample Bits:  {alice_bits[:10]}...")
        print(f"   Sample Bases: {alice_bases[:10]}...")

        #Step 2: Transmission
        qubits_reaching_bob_bits = alice_bits
        qubits_reaching_bob_bases = alice_bases

        # If Eve is present, she intercepts the photons
        if with_eavesdropper:
            print("\n2. [ALERT] Eve is intercepting the channel...")
            eve_bases = self._generate_random_bases(self.num_bits)
            eve_measured_bits = []

            for i in range(self.num_bits):
                measured_bit = self._measure_photon(alice_bits[i], alice_bases[i], eve_bases[i])
                eve_measured_bits.append(measured_bit)
            
            # Eve sends new photons to Bob based on what she measured
            qubits_reaching_bob_bits = eve_measured_bits
            qubits_reaching_bob_bases = eve_bases
        else:
            print("\n2. Photons travel through the fiber optic cable undisturbed.")

        #Step 3: Bob Measures the Photons
        bob_bases = self._generate_random_bases(self.num_bits)
        bob_results = []

        for i in range(self.num_bits):
            measured_bit = self._measure_photon(
                qubits_reaching_bob_bits[i], 
                qubits_reaching_bob_bases[i], 
                bob_bases[i]
            )
            bob_results.append(measured_bit)

        print(f"3. Bob measures received photons.")
        print(f"   Bob's Bases:   {bob_bases[:10]}...")
        print(f"   Bob's Results: {bob_results[:10]}...")

        #Step 4: The Sifting Phase
        # They discard any bits where they used different bases.
        sifted_key_alice = []
        sifted_key_bob = []

        for i in range(self.num_bits):
            if alice_bases[i] == bob_bases[i]:
                sifted_key_alice.append(alice_bits[i])
                sifted_key_bob.append(bob_results[i])

        print(f"\n4. Sifting Phase Complete.")
        print(f"   Matching Bases: {len(sifted_key_alice)} out of {self.num_bits} qubits.")

        #Step 5: Error Check
        errors = 0
        for k_alice, k_bob in zip(sifted_key_alice, sifted_key_bob):
            if k_alice != k_bob:
                errors += 1
        
        error_rate = (errors / len(sifted_key_alice)) * 100 if len(sifted_key_alice) > 0 else 0

        print("\n    FINAL REPORT ")
        print(f"Total Errors Found: {errors}")
        print(f"Error Rate (QBER):  {error_rate:.2f}%")

        if error_rate > 10: 
            print(">> CONCLUSION: UNSAFE! Eavesdropper detected or high noise.")
        else:
            print(">> CONCLUSION: SECURE! Key exchange successful.")
            print(f"   Final Key (First 10): {sifted_key_alice[:10]}...")


if __name__ == "__main__":
    sim = BB84ProtocolSimulation(num_bits=100)
    
    sim.run(with_eavesdropper=False)
    
    sim.run(with_eavesdropper=True)