import api from './api'

export interface Project {
  id: string
  title: string
  description: string | null
  status: 'draft' | 'uploaded' | 'parsing' | 'parsed' | 'optimizing' | 'ready' | 'exported' | 'archived'
  template_id: string | null
  industry: string | null
  language: string
  visibility: 'private' | 'team' | 'public'
  created_at: string
  updated_at: string
  last_exported_at: string | null
}

export interface ProjectCreateData {
  title: string
  description?: string
  industry?: string
  language?: string
  visibility?: 'private' | 'team' | 'public'
}

export interface ProjectUpdateData {
  title?: string
  description?: string
  industry?: string
  language?: string
  visibility?: 'private' | 'team' | 'public'
  status?: Project['status']
}

export const projectService = {
  // Получить список проектов
  getProjects: async (params?: {
    page?: number
    limit?: number
    status?: Project['status']
    sort?: string
  }) => {
    const response = await api.get('/api/v1/projects', { params })
    return response.data
  },

  // Создать проект
  createProject: async (data: ProjectCreateData) => {
    const response = await api.post('/api/v1/projects', data)
    return response.data
  },

  // Получить проект по ID
  getProject: async (id: string) => {
    const response = await api.get(`/api/v1/projects/${id}`)
    return response.data
  },

  // Обновить проект
  updateProject: async (id: string, data: ProjectUpdateData) => {
    const response = await api.put(`/api/v1/projects/${id}`, data)
    return response.data
  },

  // Удалить проект
  deleteProject: async (id: string) => {
    await api.delete(`/api/v1/projects/${id}`)
  },

  // Загрузить файл презентации
  uploadPresentation: async (projectId: string, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post(`/api/v1/files/${projectId}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return response.data
  },

  // Получить версии проекта
  getProjectVersions: async (projectId: string) => {
    const response = await api.get(`/api/v1/files/${projectId}/versions`)
    return response.data
  },
}
