from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_cors import CORS
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'jiyer_secret_key_2024'  # 用于session管理
CORS(app)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    # 创建公司信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_info (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            mission TEXT NOT NULL,
            vision TEXT NOT NULL,
            founded INTEGER NOT NULL,
            employees INTEGER NOT NULL,
            headquarters TEXT NOT NULL
        )
    ''')
    
    # 创建联系信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_info (
            id INTEGER PRIMARY KEY,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            working_hours TEXT NOT NULL,
            linkedin TEXT,
            twitter TEXT,
            facebook TEXT
        )
    ''')
    
    # 插入默认数据
    cursor.execute('SELECT COUNT(*) FROM company_info')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO company_info (name, description, mission, vision, founded, employees, headquarters)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'JIYER',
            'JIYER is a leading environmental technology company dedicated to creating sustainable solutions for a greener future. We specialize in innovative eco-friendly products and services that help businesses and individuals reduce their environmental impact.',
            'Our mission is to accelerate the world\'s transition to sustainable energy and environmental practices through cutting-edge technology and innovative solutions.',
            'To become the global leader in environmental technology, making sustainable living accessible to everyone.',
            2020,
            150,
            'Shenzhen, China'
        ))
    
    cursor.execute('SELECT COUNT(*) FROM contact_info')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO contact_info (address, phone, email, working_hours, linkedin, twitter, facebook)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            '123 Green Street, Shenzhen, China',
            '+86 123 4567 8900',
            'info@jiyer.com',
            'Monday - Friday: 9:00 AM - 6:00 PM',
            'https://linkedin.com/company/jiyer',
            'https://twitter.com/jiyer_eco',
            'https://facebook.com/jiyercompany'
        ))
    
    conn.commit()
    conn.close()

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/company-info')
def company_info():
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM company_info WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            'name': row[1],
            'description': row[2],
            'mission': row[3],
            'vision': row[4],
            'founded': row[5],
            'employees': row[6],
            'headquarters': row[7]
        })
    return jsonify({'error': 'Company info not found'}), 404

@app.route('/api/contact')
def contact():
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_info WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            'address': row[1],
            'phone': row[2],
            'email': row[3],
            'working_hours': row[4],
            'social_media': {
                'linkedin': row[5],
                'twitter': row[6],
                'facebook': row[7]
            }
        })
    return jsonify({'error': 'Contact info not found'}), 404

# 管理后台路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'jiyer_admin':
            session['logged_in'] = True
            return redirect(url_for('manage'))
        else:
            flash('Invalid password!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/manage')
@login_required
def manage():
    # 获取当前数据
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM company_info WHERE id = 1')
    company_data = cursor.fetchone()
    
    cursor.execute('SELECT * FROM contact_info WHERE id = 1')
    contact_data = cursor.fetchone()
    
    conn.close()
    
    return render_template('manage.html', 
                         company=company_data, 
                         contact=contact_data)

@app.route('/update_company', methods=['POST'])
@login_required
def update_company():
    try:
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE company_info 
            SET name=?, description=?, mission=?, vision=?, founded=?, employees=?, headquarters=?
            WHERE id=1
        ''', (
            request.form.get('name'),
            request.form.get('description'),
            request.form.get('mission'),
            request.form.get('vision'),
            int(request.form.get('founded')),
            int(request.form.get('employees')),
            request.form.get('headquarters')
        ))
        
        conn.commit()
        conn.close()
        flash('Company information updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating company info: {str(e)}', 'error')
    
    return redirect(url_for('manage'))

@app.route('/update_contact', methods=['POST'])
@login_required
def update_contact():
    try:
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE contact_info 
            SET address=?, phone=?, email=?, working_hours=?, linkedin=?, twitter=?, facebook=?
            WHERE id=1
        ''', (
            request.form.get('address'),
            request.form.get('phone'),
            request.form.get('email'),
            request.form.get('working_hours'),
            request.form.get('linkedin'),
            request.form.get('twitter'),
            request.form.get('facebook')
        ))
        
        conn.commit()
        conn.close()
        flash('Contact information updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating contact info: {str(e)}', 'error')
    
    return redirect(url_for('manage'))

if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(debug=True, host='0.0.0.0', port=8080)
