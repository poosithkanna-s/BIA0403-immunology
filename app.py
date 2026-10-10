from flask import Flask, render_template, request

app = Flask(__name__)

# Each condition and the symptoms that point towards it
CONDITIONS = {
    'SLE': ['photosensitivity', 'malar rash', 'hair loss', 'joint pain'],
    'Rheumatoid arthritis': ['joint pain', 'joint swelling', 'fever'],
    "Sjögren's syndrome": ['dry eyes', 'dry mouth', 'joint pain'],
    'Celiac disease': ['diarrhea', 'bloating', 'fatigue'],
    'Primary immunodeficiency': ['recurrent infections', 'fatigue'],
    'Allergic disorder': ['wheezing', 'hives', 'skin rash'],
}

# The 20 standard amino-acid one-letter codes
VALID_AA = set('ACDEFGHIKLMNPQRSTVWY')
HYDROPHOBIC = set('AILMFWVY')
HYDROPHILIC = set('DERKHNQST')


def clean_sequence(raw):
    """Drop FASTA header lines (starting with '>'), remove all whitespace, uppercase."""
    lines = [line for line in raw.splitlines() if not line.strip().startswith('>')]
    return ''.join(''.join(lines).split()).upper()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    results = None
    error = None

    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')

        # Lab values: an empty box counts as 0
        try:
            ana = float(request.form.get('ana') or 0)
            dsdna = float(request.form.get('dsdna') or 0)
            rf = float(request.form.get('rf') or 0)
            crp = float(request.form.get('crp') or 0)
        except ValueError:
            error = 'Please enter valid numerical laboratory values.'

        if not error:
            rows = []

            for name, clues in CONDITIONS.items():
                score = 0
                factors = []

                # 15 points for every symptom that matches this condition
                for symptom in symptoms:
                    if symptom in clues:
                        score += 15
                        factors.append(symptom.title())

                # Extra points from lab values
                if name == 'SLE':
                    if ana >= 80:
                        score += 25
                        factors.append('Raised ANA titre')
                    if dsdna >= 10:
                        score += 30
                        factors.append('Raised anti-dsDNA')

                elif name == 'Rheumatoid arthritis':
                    if rf >= 20:
                        score += 25
                        factors.append('Raised RF')
                    if crp >= 10:
                        score += 15
                        factors.append('Raised CRP')

                elif name == 'Allergic disorder':
                    ige = request.form.get('ige')
                    if ige:
                        try:
                            if float(ige) >= 150:
                                score += 20
                                factors.append('Raised IgE')
                        except ValueError:
                            pass

                score = min(score, 100)
                rows.append({
                    'name': name,
                    'score': score,
                    'factors': factors or ['No strong matching feature'],
                })

            # Highest score first
            results = sorted(rows, key=lambda row: row['score'], reverse=True)

    return render_template('diagnosis.html', results=results, error=error)


@app.route('/antigen', methods=['GET', 'POST'])
def antigen():
    result = None
    error = None

    if request.method == 'POST':
        seq = clean_sequence(request.form.get('sequence', ''))

        if not seq:
            error = 'Enter a protein sequence.'
        elif len(seq) > 5000:
            error = 'For this small demonstration, sequences are limited to 5000 residues.'
        elif set(seq) - VALID_AA:
            error = 'Invalid amino-acid sequence. Use standard one-letter amino-acid codes.'
        else:
            # Percentage of hydrophobic residues
            hydrophobicity = sum(a in HYDROPHOBIC for a in seq) / len(seq) * 100

            # Slide a 9-residue window along the sequence and keep the
            # windows where at least 6 residues are hydrophilic
            hydrophilic_regions = []
            for i in range(max(0, len(seq) - 8)):
                window = seq[i:i + 9]
                if sum(a in HYDROPHILIC for a in window) >= 6:
                    hydrophilic_regions.append((i + 1, i + 9, window))

            antigenicity = 35 + len(hydrophilic_regions[:10]) * 6 + (100 - hydrophobicity) * 0.3

            result = {
                'length': len(seq),
                'hydrophobicity': round(hydrophobicity),
                'hydrophilic': hydrophilic_regions[:5],
                'antigenicity': min(100, round(antigenicity)),
            }

    return render_template('antigen.html', result=result, error=error)


@app.route('/interaction', methods=['GET', 'POST'])
def interaction():
    result = None
    error = None

    if request.method == 'POST':
        a = clean_sequence(request.form.get('antigen', ''))
        b = clean_sequence(request.form.get('receptor', ''))

        if not a or not b or set(a + b) - VALID_AA:
            error = 'Enter two valid protein sequences using standard amino-acid codes.'
        else:
            # Fraction of hydrophobic residues in each sequence
            hyd_a = sum(x in HYDROPHOBIC for x in a) / len(a)
            hyd_b = sum(x in HYDROPHOBIC for x in b) / len(b)

            # Net charge: K and R are positive, D and E are negative
            charge_a = sum(x in 'KR' for x in a) - sum(x in 'DE' for x in a)
            charge_b = sum(x in 'KR' for x in b) - sum(x in 'DE' for x in b)

            # Start at 70, subtract for differences in hydrophobicity and charge
            score = 70 - abs(hyd_a - hyd_b) * 50 - abs(charge_a / len(a) - charge_b / len(b)) * 80
            result = round(max(0, min(100, score)))

    return render_template('interaction.html', result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)