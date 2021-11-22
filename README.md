# Covid Pass Verifier

## How it works
Sends a fetch request to tthe server.
Request body:
```json
{
	"uri": "NZCP:/1/2KCEVI...NCFDX"
}
```
On success:
```json
{
	"claims": {
		"@context": [
			"https://www.w3.org/2018/credentials/v1",
			"https://nzcp.covid19.health.nz/contexts/v1"
		],
		"credentialSubject": {
			"dob": "1960-04-16",
			"familyName": "Sparrow",
			"givenName": "Jack"
		},
		"type": ["VerifiableCredential", "PublicCovidPass"],
		"version": "1.0.0"
	},
	"success": true
}
```
On error:
```json
{
	"error": "Failed to verify.",
	"success": false
}
```