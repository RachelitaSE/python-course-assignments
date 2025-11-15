import cpi

'''this module calculates the cpi in different regeions in the US, using dollars'''
cpi.update()
new= cpi.inflate(10000,2000, to=2020, area="U.S. city average")
print(new)