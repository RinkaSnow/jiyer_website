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
    
    # 创建产品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建产品图片表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            is_primary BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
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

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('index.html')

@app.route('/contact')
def contact_page():
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

# 产品相关API
@app.route('/api/products')
def get_products():
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    # 获取所有产品，按分类分组
    cursor.execute('''
        SELECT p.*, 
               GROUP_CONCAT(pi.image_path ORDER BY pi.is_primary DESC) as images,
               GROUP_CONCAT(pi.is_primary ORDER BY pi.is_primary DESC) as primary_flags
        FROM products p
        LEFT JOIN product_images pi ON p.id = pi.product_id
        GROUP BY p.id
        ORDER BY p.category, p.name
    ''')
    
    products = []
    for row in cursor.fetchall():
        images = row[7].split(',') if row[7] else []
        primary_flags = row[8].split(',') if row[8] else []
        
        # 确保主图排在第一位
        image_data = []
        for i, img in enumerate(images):
            is_primary = primary_flags[i] == '1' if i < len(primary_flags) else False
            image_data.append({'path': img, 'is_primary': is_primary})
        
        # 按主图排序
        image_data.sort(key=lambda x: not x['is_primary'])
        
        product = {
            'id': row[0],
            'category': row[1],
            'name': row[2],
            'code': row[3],
            'description': row[4],
            'images': [img['path'] for img in image_data]
        }
        products.append(product)
    
    conn.close()
    return jsonify({'products': products})

@app.route('/api/products/<int:product_id>')
def get_product_detail(product_id):
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, 
               GROUP_CONCAT(pi.image_path) as images,
               GROUP_CONCAT(pi.is_primary) as primary_flags
        FROM products p
        LEFT JOIN product_images pi ON p.id = pi.product_id
        WHERE p.id = ?
        GROUP BY p.id
    ''', (product_id,))
    
    row = cursor.fetchone()
    if row:
        images = row[7].split(',') if row[7] else []
        primary_flags = row[8].split(',') if row[8] else []
        
        # 重新排序图片，主图在前
        image_data = []
        for i, img in enumerate(images):
            is_primary = primary_flags[i] == '1' if i < len(primary_flags) else False
            image_data.append({'path': img, 'is_primary': is_primary})
        
        # 按主图排序
        image_data.sort(key=lambda x: not x['is_primary'])
        
        product = {
            'id': row[0],
            'category': row[1],
            'name': row[2],
            'code': row[3],
            'description': row[4],
            'images': [img['path'] for img in image_data]
        }
        conn.close()
        return jsonify(product)
    
    conn.close()
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/categories')
def get_categories():
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({'categories': categories})

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
    return render_template('manage.html')

@app.route('/manage/company')
@login_required
def manage_company():
    # 获取当前数据
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM company_info WHERE id = 1')
    company_data = cursor.fetchone()
    
    conn.close()
    
    return render_template('manage_company.html', company=company_data)

@app.route('/manage/products')
@login_required
def manage_products():
    # 获取产品数据
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, 
               GROUP_CONCAT(pi.image_path ORDER BY pi.is_primary DESC) as images,
               GROUP_CONCAT(pi.is_primary ORDER BY pi.is_primary DESC) as primary_flags
        FROM products p
        LEFT JOIN product_images pi ON p.id = pi.product_id
        GROUP BY p.id
        ORDER BY p.category, p.name
    ''')
    products_data = cursor.fetchall()
    
    # 获取分类数据
    cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('manage_products.html', products=products_data, categories=categories)

@app.route('/manage/contact')
@login_required
def manage_contact():
    # 获取当前数据
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contact_info WHERE id = 1')
    contact_data = cursor.fetchone()
    
    conn.close()
    
    return render_template('manage_contact.html', contact=contact_data)

@app.route('/edit_product/<int:product_id>')
@login_required
def edit_product(product_id):
    # 获取产品数据
    conn = sqlite3.connect('jiyer.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, 
               GROUP_CONCAT(pi.image_path) as images
        FROM products p
        LEFT JOIN product_images pi ON p.id = pi.product_id
        WHERE p.id = ?
        GROUP BY p.id
    ''', (product_id,))
    
    product_data = cursor.fetchone()
    conn.close()
    
    if not product_data:
        flash('Product not found!', 'error')
        return redirect(url_for('manage_products'))
    
    return render_template('edit_product.html', product=product_data)

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
    
    return redirect(url_for('manage_company'))

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
    
    return redirect(url_for('manage_contact'))

# 产品管理路由
@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    try:
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (category, name, code, description)
            VALUES (?, ?, ?, ?)
        ''', (
            request.form.get('category'),
            request.form.get('name'),
            request.form.get('code'),
            request.form.get('description')
        ))
        
        product_id = cursor.lastrowid
        
        # 处理图片上传
        images = request.files.getlist('images')
        for i, image in enumerate(images):
            if image.filename:
                filename = f"product_{product_id}_{i}_{image.filename}"
                image_path = f"/static/images/products/{filename}"
                image.save(f"static/images/products/{filename}")
                
                cursor.execute('''
                    INSERT INTO product_images (product_id, image_path, is_primary)
                    VALUES (?, ?, ?)
                ''', (product_id, image_path, i == 0))  # 第一张图片设为主图
        
        conn.commit()
        conn.close()
        flash('Product added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding product: {str(e)}', 'error')
    
    return redirect(url_for('manage_products'))

@app.route('/update_product', methods=['POST'])
@login_required
def update_product():
    try:
        product_id = request.form.get('product_id')
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products 
            SET category=?, name=?, code=?, description=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (
            request.form.get('category'),
            request.form.get('name'),
            request.form.get('code'),
            request.form.get('description'),
            product_id
        ))
        
        # 处理新图片上传
        images = request.files.getlist('images')
        for i, image in enumerate(images):
            if image.filename:
                filename = f"product_{product_id}_{i}_{image.filename}"
                image_path = f"/static/images/products/{filename}"
                image.save(f"static/images/products/{filename}")
                
                cursor.execute('''
                    INSERT INTO product_images (product_id, image_path, is_primary)
                    VALUES (?, ?, ?)
                ''', (product_id, image_path, False))
        
        conn.commit()
        conn.close()
        flash('Product updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating product: {str(e)}', 'error')
    
    product_id = request.form.get('product_id')
    return redirect(url_for('edit_product', product_id=product_id))

@app.route('/delete_product', methods=['POST'])
@login_required
def delete_product():
    try:
        product_id = request.form.get('product_id')
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        # 删除产品图片文件
        cursor.execute('SELECT image_path FROM product_images WHERE product_id = ?', (product_id,))
        images = cursor.fetchall()
        for image in images:
            try:
                os.remove(f"static/images/products/{image[0].split('/')[-1]}")
            except:
                pass  # 忽略文件删除错误
        
        # 删除产品
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        
        conn.commit()
        conn.close()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')
    
    return redirect(url_for('manage_products'))

@app.route('/delete_product_image', methods=['POST'])
@login_required
def delete_product_image():
    try:
        image_path = request.form.get('image_path')
        product_id = request.form.get('product_id')
        
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        # 删除图片记录
        cursor.execute('DELETE FROM product_images WHERE product_id = ? AND image_path = ?', (product_id, image_path))
        
        # 删除图片文件
        try:
            filename = image_path.split('/')[-1]
            os.remove(f"static/images/products/{filename}")
        except:
            pass  # 忽略文件删除错误
        
        conn.commit()
        conn.close()
        flash('Image deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting image: {str(e)}', 'error')
    
    product_id = request.form.get('product_id')
    return redirect(url_for('edit_product', product_id=product_id))

@app.route('/set_primary_image', methods=['POST'])
@login_required
def set_primary_image():
    try:
        product_id = request.form.get('product_id')
        image_path = request.form.get('image_path')
        
        conn = sqlite3.connect('jiyer.db')
        cursor = conn.cursor()
        
        # 先将所有图片设置为非主图
        cursor.execute('UPDATE product_images SET is_primary = 0 WHERE product_id = ?', (product_id,))
        
        # 将选中的图片设置为主图
        cursor.execute('UPDATE product_images SET is_primary = 1 WHERE product_id = ? AND image_path = ?', (product_id, image_path))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(debug=True, host='0.0.0.0', port=80)
