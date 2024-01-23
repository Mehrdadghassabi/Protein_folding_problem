import chargefw2_python
# molecules = chargefw2_python.Molecules('AF-A0A2K5QXN6-F1-model_v4.pdb')
# or
molecules = chargefw2_python.Molecules('AF-A0A2K5QXN6-F1-model_v4-Cleared.pdb')

# Caculate Charge of Every Atoms by thire id oerder
charges_sqeqp = chargefw2_python.calculate_charges(molecules, 'sqeqp', 'SQEqp_10_Schindler2021_CCD_gen')
print(charges_sqeqp["AF-A0A2K5QXN6-F1-model_v4-Cleared"])