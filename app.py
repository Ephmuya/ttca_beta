from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '5141'
app.config['MYSQL_DATABASE_DB'] = 'ncttca_gis'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/')
def index():
	return render_template('index.html')
# Creating APIs

@app.route('/indicator/transit')
def ke_node():
	cur = mysql.connect().cursor()
	cur.execute('''

SELECT subnodelink.`Name`,
subnodelink.country, 
subnodelink.indicator,
subnodelink.nodeid,
subnodelink.routeid,
indicatorgroup.id,
indicatorgroup.title
FROM subnodelink  JOIN indicatorgroup WHERE 
subnodelink.`indicator ID` = indicatorgroup.id
AND indicatorgroup.title = 'Transit Time and Delays'

     ''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'node': r})


@app.route('/api/country')
def country():
	cur = mysql.connect().cursor()
	cur.execute('''
	SELECT * FROM country;

	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'country': r})


# ....Volume & Capacity ....... #

# 1. indicators
# VC KE
@app.route('/api/vc/indicators/ke')
def vcindicatorske():
	cur = mysql.connect().cursor()
	cur.execute('''
		SELECT 
		volumecapacity.title,
		volumecapacity.countryid,
		volumecapacity.referencetable
		FROM volumecapacity	
		WHERE volumecapacity.countryid = 'KE'

	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'records': r})


# VC UG
@app.route('/api/vc/indicators/ug')
def vcindicatorsug():
	cur = mysql.connect().cursor()
	cur.execute('''
		SELECT 
		volumecapacity.title,
		volumecapacity.countryid
		FROM volumecapacity	

	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'vcindicatorsug': r})


# VC RW
@app.route('/api/vc/indicators/rw')
def vcindicatorsrw():
	cur = mysql.connect().cursor()
	cur.execute('''
		SELECT 
		volumecapacity.title,
		volumecapacity.countryid
		FROM volumecapacity	
		WHERE volumecapacity.countryid = 'RW'
	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'vcindicatorsrw': r})


# VC DRC
@app.route('/api/vc/indicators/drc')
def vcindicatorsdrc():
	cur = mysql.connect().cursor()
	cur.execute('''
		SELECT 
		volumecapacity.title,
		volumecapacity.countryid
		FROM volumecapacity	
		WHERE volumecapacity.countryid = 'CD'
	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'vcindicatorsDRC': r})


# VC SS
@app.route('/api/vc/indicators/ss')
def vcindicatorsss():
	cur = mysql.connect().cursor()
	cur.execute('''
		SELECT 
		volumecapacity.title,
		volumecapacity.countryid
		FROM volumecapacity	
		WHERE volumecapacity.countryid = 'SS'
	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'vcindicatorsss': r})


# VC SS
@app.route('/api/vc/indicators/bi')
def vcindicatorsbi():
	cur = mysql.connect().cursor()
	cur.execute('''
		SELECT 
		volumecapacity.title,
		volumecapacity.countryid
		FROM volumecapacity	
		WHERE volumecapacity.countryid = 'BI'
	''')
	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'vcindicatorsbi': r})


# 2.  allnoncontcargo
@app.route('/api/vc/indicators/ke/allnoncontcargo')
def allnoncontcargo():
	cur = mysql.connect().cursor()
	cur.execute("""
	SELECT 
allnoncontcargo.year,
ROUND(SUM(allnoncontcargo.minweight), 2)  as minweight,
ROUND(SUM(allnoncontcargo.maxweight), 2)  as maxweight,
ROUND(SUM(allnoncontcargo.avgweight), 2)  as avgweight,
ROUND(SUM(allnoncontcargo.stdweight), 2)  as stdweight,
ROUND(SUM(allnoncontcargo.totalweight), 2)  as totalweight
FROM allnoncontcargo
GROUP BY allnoncontcargo.year
	""")

	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'records': r})


# VC imports and Exports
# 1. Monthly
@app.route('/api/vc/indicators/ke/importsexports/m')
def importsexports_m():
	cur = mysql.connect().cursor()
	cur.execute("""
		SELECT `Year` , `Month`, 
			sum(`Total Export Weight`) AS 'Exports', 
			sum(`Total Import Weight (Tonne)`) AS 'Imports'
		FROM importsexports
		GROUP BY importsexports.`Year` , importsexports.`Month`
	""")

	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'records': r})

# 2. Quayerly
@app.route('/api/vc/indicators/ke/importsexports/q')
def importsexports_q():
	cur = mysql.connect().cursor()
	cur.execute("""
SELECT `Year` ,
CASE WHEN importsexports.MonthID BETWEEN 0 AND 3 THEN 'Q1: January - March'
	WHEN importsexports.MonthID BETWEEN 4 AND 6 THEN 'Q2: April - June'
	WHEN importsexports.MonthID BETWEEN 7 AND 9 THEN 'Q3: July - September'
	ELSE 'Q4: October - December'
END AS `period`,
ROUND(sum(`Total Export Weight`),2) AS 'Exports',
ROUND(sum(`Total Import Weight (Tonne)`),2) AS 'Imports'
FROM importsexports
GROUP BY importsexports.`Year`, `period` 
	""")

	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'records': r})

# 3. Yearly
@app.route('/api/vc/indicators/ke/importsexports/y')
def importsexports_y():
	cur = mysql.connect().cursor()
	cur.execute("""
		SELECT `Year` , sum(`Total Export Weight`) AS 'Exports', sum(`Total Import Weight (Tonne)`) AS 'Imports'
		FROM importsexports
		GROUP BY importsexports.`Year`
	""")

	r = [dict((cur.description[i][0], value)
	          for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'records': r})



if __name__ == '__main__':
	app.run(debug=True)