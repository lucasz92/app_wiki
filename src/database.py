"""
Gestor de base de datos SQLite para WikiApp
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "wiki.db"):
        self.db_path = db_path
        
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Inicializa las tablas de la base de datos"""
        with self.get_connection() as conn:
            # Tabla de categorías
            conn.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    color TEXT DEFAULT '#3498db',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de artículos
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category_id INTEGER,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            # Insertar categorías por defecto
            default_categories = [
                ("Higiene y Seguridad", "Documentación sobre normas de seguridad e higiene", "#e74c3c"),
                ("Metodología 5S", "Documentación sobre metodología 5S", "#f39c12"),
                ("Tutorial", "Tutoriales y guías paso a paso", "#2ecc71"),
                ("Procesos", "Documentación de procesos organizacionales", "#9b59b6"),
                ("General", "Documentación general", "#34495e")
            ]
            
            for name, desc, color in default_categories:
                conn.execute("""
                    INSERT OR IGNORE INTO categories (name, description, color)
                    VALUES (?, ?, ?)
                """, (name, desc, color))
            
            conn.commit()
    
    def create_article(self, title: str, content: str, category_id: int, tags: str = "") -> int:
        """Crea un nuevo artículo"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO articles (title, content, category_id, tags)
                VALUES (?, ?, ?, ?)
            """, (title, content, category_id, tags))
            return cursor.lastrowid
    
    def get_articles(self, category_id: Optional[int] = None, search_term: str = "") -> List[Dict]:
        """Obtiene lista de artículos"""
        with self.get_connection() as conn:
            query = """
                SELECT a.*, c.name as category_name, c.color as category_color
                FROM articles a
                LEFT JOIN categories c ON a.category_id = c.id
                WHERE 1=1
            """
            params = []
            
            if category_id:
                query += " AND a.category_id = ?"
                params.append(category_id)
            
            if search_term:
                query += " AND (a.title LIKE ? OR a.content LIKE ? OR a.tags LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            query += " ORDER BY a.updated_at DESC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_article(self, article_id: int) -> Optional[Dict]:
        """Obtiene un artículo específico"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT a.*, c.name as category_name, c.color as category_color
                FROM articles a
                LEFT JOIN categories c ON a.category_id = c.id
                WHERE a.id = ?
            """, (article_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_article(self, article_id: int, title: str, content: str, category_id: int, tags: str = ""):
        """Actualiza un artículo"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE articles 
                SET title = ?, content = ?, category_id = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (title, content, category_id, tags, article_id))
    
    def delete_article(self, article_id: int):
        """Elimina un artículo"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    
    def get_categories(self) -> List[Dict]:
        """Obtiene todas las categorías"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM categories ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]
    
    def create_category(self, name: str, description: str = "", color: str = "#3498db") -> int:
        """Crea una nueva categoría"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO categories (name, description, color)
                VALUES (?, ?, ?)
            """, (name, description, color))
            return cursor.lastrowid