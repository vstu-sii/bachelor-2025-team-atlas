import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { motion } from 'framer-motion'
import Head from 'next/head'
import { FiRocket, FiFileText, FiStar, FiZap } from 'react-icons/fi'
import Button from '@/components/common/Button'
import { useAuth } from '@/hooks/useAuth'

export default function Home() {
  const router = useRouter()
  const { isAuthenticated, user } = useAuth()
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, router])

  const handleGetStarted = () => {
    setIsLoading(true)
    // Telegram авторизация
    window.Telegram?.Login?.auth(
      { bot_id: process.env.NEXT_PUBLIC_TELEGRAM_BOT_ID, request_access: true },
      (data) => {
        console.log('Telegram auth data:', data)
        // Здесь будет вызов API для аутентификации
        router.push('/dashboard')
      }
    )
  }

  const features = [
    {
      icon: <FiZap className="h-8 w-8" />,
      title: 'AI-оптимизация',
      description: 'GPT-4 автоматически улучшает тексты и структуру вашей презентации',
    },
    {
      icon: <FiFileText className="h-8 w-8" />,
      title: 'Профессиональные шаблоны',
      description: 'Готовые дизайны для любых сфер: от стартапов до корпоративных презентаций',
    },
    {
      icon: <FiRocket className="h-8 w-8" />,
      title: 'Быстрый результат',
      description: 'Первая презентация за 10 минут без навыков дизайна',
    },
    {
      icon: <FiStar className="h-8 w-8" />,
      title: 'Экспорт в один клик',
      description: 'PPTX и PDF форматы, готовые к отправке инвесторам',
    },
  ]

  return (
    <>
      <Head>
        <title>AutoPitch - Генератор питч-презентаций для стартапов</title>
        <meta name="description" content="Создавайте профессиональные питч-деки с помощью AI за 10 минут" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        {/* Hero Section */}
        <nav className="px-6 py-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-pitch-blue rounded-lg"></div>
              <span className="text-xl font-bold text-gray-900">AutoPitch</span>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="secondary" onClick={() => router.push('/login')}>
                Вход
              </Button>
              <Button onClick={handleGetStarted} loading={isLoading}>
                Начать бесплатно
              </Button>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-6 py-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Создавайте питч-деки с{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pitch-blue to-purple-600">
                AI
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
              Профессиональные презентации для инвесторов за 10 минут. 
              Без дизайнерских навыков. С AI-оптимизацией текста.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Button size="lg" onClick={handleGetStarted} loading={isLoading}>
                <FiRocket className="mr-2" />
                Начать с AI
              </Button>
              <Button variant="secondary" size="lg" onClick={() => router.push('/templates')}>
                Посмотреть шаблоны
              </Button>
            </div>
          </motion.div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-pitch-blue mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>

          {/* CTA Section */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-gradient-to-r from-pitch-blue to-blue-600 rounded-2xl p-8 md:p-12 text-center text-white"
          >
            <h2 className="text-3xl font-bold mb-4">Готовы покорить инвесторов?</h2>
            <p className="text-blue-100 mb-8 max-w-2xl mx-auto">
              Присоединяйтесь к 1000+ предпринимателей, которые уже создали свои питч-деки с AutoPitch
            </p>
            <Button
              variant="white"
              size="lg"
              onClick={handleGetStarted}
              loading={isLoading}
            >
              Создать первую презентацию
            </Button>
          </motion.div>
        </main>

        <footer className="mt-20 py-8 px-6 border-t border-gray-200">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="mb-4 md:mb-0">
                <div className="flex items-center space-x-2">
                  <div className="h-6 w-6 bg-pitch-blue rounded"></div>
                  <span className="font-bold text-gray-900">AutoPitch</span>
                </div>
                <p className="text-gray-600 text-sm mt-2">
                  Генератор питч-презентаций для стартапов
                </p>
              </div>
              <div className="flex space-x-6">
                <a href="#" className="text-gray-600 hover:text-gray-900">
                  Условия
                </a>
                <a href="#" className="text-gray-600 hover:text-gray-900">
                  Конфиденциальность
                </a>
                <a href="#" className="text-gray-600 hover:text-gray-900">
                  Контакты
                </a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
