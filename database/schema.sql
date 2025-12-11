CREATE DATABASE IF NOT EXISTS autopitch;
USE autopitch;

CREATE TABLE Users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username_id BIGINT UNIQUE NOT NULL,                    
    username VARCHAR(255),                                              
    email VARCHAR(255),                                   
    subscription_tier ENUM('free', 'pro', 'business') DEFAULT 'free',
    projects_limit INT UNSIGNED DEFAULT 3,                 
    export_limit_daily INT UNSIGNED DEFAULT 5,             
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    settings JSON DEFAULT '{"notifications": true, "theme": "light"}',
    INDEX idx_telegram_id (username_id),
    INDEX idx_subscription_tier (subscription_tier),
    INDEX idx_created_at (created_at)
);

CREATE TABLE Projects (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),              
    user_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(255) NOT NULL DEFAULT 'Новая презентация',
    description TEXT,
    status ENUM('draft', 'uploaded', 'parsing', 'parsed', 'optimizing', 'ready', 'exported', 'archived') DEFAULT 'draft',
    template_id VARCHAR(100) DEFAULT 'default',           
    industry VARCHAR(100),                                 
    language ENUM('ru', 'en') DEFAULT 'ru',
    visibility ENUM('private', 'team', 'public') DEFAULT 'private',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_exported_at TIMESTAMP NULL,
    metadata JSON,                                        
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_user_status (user_id, status),
    INDEX idx_template (template_id)
);


CREATE TABLE PresentationFiles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    version_number INT UNSIGNED DEFAULT 1,
    file_type ENUM('pptx', 'pdf') NOT NULL,
    source_type ENUM('upload', 'generated', 'imported') DEFAULT 'upload',
    original_filename VARCHAR(255),
    file_size BIGINT UNSIGNED,                           
    storage_path VARCHAR(500) NOT NULL,                   
    md5_hash CHAR(32),                                    
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parsing_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    parsing_started_at TIMESTAMP NULL,
    parsing_completed_at TIMESTAMP NULL,
    parsing_errors TEXT,
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_version (project_id, version_number),
    INDEX idx_project_id (project_id),
    INDEX idx_parsing_status (parsing_status),
    INDEX idx_upload_date (upload_date)
);


CREATE TABLE Slides (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    version_id CHAR(36) NOT NULL,
    slide_number INT UNSIGNED NOT NULL,
    slide_type ENUM('title', 'problem', 'solution', 'market', 'product', 
                   'business_model', 'team', 'traction', 'financials', 
                   'competitors', 'roadmap', 'contact', 'other') DEFAULT 'other',
    original_content JSON,                               
    optimized_content JSON,                              
    applied_template JSON,                              
    layout_type VARCHAR(50) DEFAULT 'standard',
    ai_feedback TEXT,                                    
    is_modified BOOLEAN DEFAULT FALSE,                    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE,
    FOREIGN KEY (version_id) REFERENCES PresentationFiles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_slide_version (version_id, slide_number),
    INDEX idx_project_version (project_id, version_id),
    INDEX idx_slide_type (slide_type),
    INDEX idx_slide_number (slide_number)
);


CREATE TABLE AI_Operations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    operation_type ENUM('parse', 'optimize', 'generate', 'design', 'analyze_market') NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    llm_model VARCHAR(50) DEFAULT 'gpt-4',
    prompt_version VARCHAR(20) DEFAULT '1.0',
    input_data JSON,                                      
    output_data JSON,                                     
    tokens_used INT UNSIGNED DEFAULT 0,
    processing_time_ms INT UNSIGNED,
    cost_estimate DECIMAL(10,6) DEFAULT 0.000000,
    error_message TEXT,
    retry_count INT UNSIGNED DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_operation_type (operation_type),
    INDEX idx_status (status),
    INDEX idx_started_at (started_at),
    INDEX idx_project_status (project_id, status)
);


CREATE TABLE Templates (
    id VARCHAR(100) PRIMARY KEY,                         
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category ENUM('professional', 'creative', 'minimal', 'corporate', 'startup') DEFAULT 'professional',
    industry_focus JSON DEFAULT '[]',                     
    config_schema JSON NOT NULL,                          
    thumbnail_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    version VARCHAR(20) DEFAULT '1.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_is_active (is_active),
    INDEX idx_is_premium (is_premium)
);


CREATE TABLE Exports (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    export_format ENUM('pptx', 'pdf', 'both') NOT NULL,
    export_type ENUM('full', 'summary', 'pitch') DEFAULT 'full',
    quality ENUM('standard', 'high') DEFAULT 'standard',
    file_size BIGINT UNSIGNED,
    download_url VARCHAR(500),
    expires_at TIMESTAMP NULL,                            
    status ENUM('processing', 'completed', 'failed') DEFAULT 'processing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status)
);


CREATE TABLE UsageStats (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    date DATE NOT NULL,
    projects_created INT UNSIGNED DEFAULT 0,
    files_uploaded INT UNSIGNED DEFAULT 0,
    ai_operations INT UNSIGNED DEFAULT 0,
    exports_count INT UNSIGNED DEFAULT 0,
    tokens_used_total INT UNSIGNED DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, date),
    INDEX idx_user_id (user_id),
    INDEX idx_date (date)
);


CREATE TABLE AI_Cache (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prompt_hash CHAR(64) NOT NULL,                        
    model VARCHAR(50) NOT NULL,
    prompt_version VARCHAR(20) NOT NULL,
    response_json JSON NOT NULL,
    tokens_used INT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INT UNSIGNED DEFAULT 0,
    UNIQUE KEY unique_prompt_hash (prompt_hash, model, prompt_version),
    INDEX idx_prompt_hash (prompt_hash),
    INDEX idx_created_at (created_at),
    INDEX idx_last_accessed (last_accessed)
);


CREATE TABLE SystemSettings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value JSON,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,                      
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_setting_key (setting_key),
    INDEX idx_is_public (is_public)
);

DELIMITER //
CREATE TRIGGER after_project_create
    AFTER INSERT ON Projects
    FOR EACH ROW
BEGIN
    INSERT INTO UsageStats (user_id, date, projects_created)
    VALUES (NEW.user_id, CURDATE(), 1)
    ON DUPLICATE KEY UPDATE 
        projects_created = projects_created + 1,
        date = CURDATE();
END//


CREATE TRIGGER after_export_complete
    AFTER UPDATE ON Exports
    FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
    
        INSERT INTO UsageStats (user_id, date, exports_count)
        VALUES (NEW.user_id, CURDATE(), 1)
        ON DUPLICATE KEY UPDATE 
            exports_count = exports_count + 1;
            
        UPDATE Projects 
        SET last_exported_at = CURRENT_TIMESTAMP
        WHERE id = NEW.project_id;
    END IF;
END//

CREATE TRIGGER update_ai_cache_access
    BEFORE UPDATE ON AI_Cache
    FOR EACH ROW
BEGIN
    SET NEW.last_accessed = CURRENT_TIMESTAMP;
    SET NEW.access_count = OLD.access_count + 1;
END//
DELIMITER ;



INSERT INTO Templates (id, name, description, category, config_schema, is_premium) VALUES
('default', 'Стандартный', 'Чистый профессиональный шаблон', 'professional', '{"colors": {"primary": "#2563eb", "secondary": "#1e293b"}, "fonts": {"heading": "Inter", "body": "Inter"}, "layouts": ["title", "split", "full"]}', FALSE),
('venture', 'Венчурный', 'Для питчей инвесторам', 'startup', '{"colors": {"primary": "#7c3aed", "secondary": "#4f46e5"}, "fonts": {"heading": "Montserrat", "body": "Open Sans"}, "layouts": ["title", "focus", "grid"]}', FALSE),
('corporate', 'Корпоративный', 'Формальный стиль для B2B', 'corporate', '{"colors": {"primary": "#0f172a", "secondary": "#475569"}, "fonts": {"heading": "Roboto", "body": "Roboto"}, "layouts": ["title", "classic", "minimal"]}', TRUE);


INSERT INTO SystemSettings (setting_key, setting_value, description, is_public) VALUES
('subscription_limits', '{"free": {"projects": 3, "exports_per_day": 5, "ai_operations": 20}, "pro": {"projects": 50, "exports_per_day": 50, "ai_operations": 500}, "business": {"projects": 1000, "exports_per_day": 200, "ai_operations": 5000}}', 'Лимиты по подпискам', TRUE),
('file_limits', '{"max_size_mb": 100, "allowed_types": ["pptx", "pdf"], "max_pages": 50}', 'Ограничения файлов', TRUE),
('ai_settings', '{"default_model": "gpt-4", "fallback_model": "gpt-3.5-turbo", "max_tokens": 4000, "timeout_seconds": 30}', 'Настройки AI', FALSE),
('export_settings', '{"pptx_quality": "high", "pdf_dpi": 150, "link_expiry_hours": 24}', 'Настройки экспорта', FALSE),
('supported_languages', '["ru", "en"]', 'Поддерживаемые языки', TRUE);


CREATE USER 'autopitch_user'@'%' IDENTIFIED BY 'StrongPass!2024';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON autopitch.* TO 'autopitch_user'@'%';
FLUSH PRIVILEGES;

CREATE INDEX idx_slides_content ON Slides((CAST(optimized_content AS CHAR(1000))));
CREATE INDEX idx_ai_cache_response ON AI_Cache((CAST(response_json AS CHAR(1000))));
CREATE INDEX idx_projects_metadata ON Projects((CAST(metadata AS CHAR(1000))));

