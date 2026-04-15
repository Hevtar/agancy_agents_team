'use client';

import { useEffect, useState } from 'react';
import { api, DashboardStats, Project, Task, Blocker, Agent } from '@/lib/api';
import {
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock,
  FolderOpen,
  LayoutDashboard,
  ListTodo,
  PieChart,
  Play,
  Users,
  Wallet,
} from 'lucide-react';

export default function HomePage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        // Set a demo token for development (replace with real auth)
        api.setToken('demo-token');

        const [dashboardData, projectsData, tasksData, agentsData] = await Promise.all([
          api.getDashboardStats(),
          api.getProjects({ page_size: 5 }),
          api.getTasks({ page_size: 5 }),
          api.getAgents(),
        ]);

        setStats(dashboardData);
        setProjects(projectsData.items);
        setTasks(tasksData.items);
        setAgents(agentsData.items);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-12 h-12 text-blue-500 animate-pulse mx-auto mb-4" />
          <p className="text-gray-600">Загрузка...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <LayoutDashboard className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Agency Agents</h1>
                <p className="text-sm text-gray-500">Панель управления маркетинговым агентством</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {new Date().toLocaleDateString('ru-RU', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { name: 'Обзор', href: '#', icon: LayoutDashboard, active: true },
              { name: 'Проекты', href: '#projects', icon: FolderOpen },
              { name: 'Задачи', href: '#tasks', icon: ListTodo },
              { name: 'Блокеры', href: '#blockers', icon: AlertTriangle },
              { name: 'Агенты', href: '#agents', icon: Users },
              { name: 'Аналитика', href: '#analytics', icon: PieChart },
            ].map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={`flex items-center px-1 py-4 border-b-2 text-sm font-medium transition-colors ${
                  item.active
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <item.icon className="w-4 h-4 mr-2" />
                {item.name}
              </a>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Активные проекты"
              value={stats.active_projects}
              total={stats.total_projects}
              icon={FolderOpen}
              color="blue"
            />
            <StatCard
              title="Ожидающие задачи"
              value={stats.pending_tasks}
              total={stats.total_tasks}
              icon={ListTodo}
              color="green"
            />
            <StatCard
              title="Открытые блокеры"
              value={stats.open_blockers}
              critical={stats.critical_blockers}
              icon={AlertTriangle}
              color="red"
            />
            <StatCard
              title="Токены сегодня"
              value={stats.tokens_used_today}
              total={stats.daily_token_budget}
              icon={Wallet}
              color="purple"
            />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Projects List */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Последние проекты</h2>
              <button className="text-sm text-blue-600 hover:text-blue-800">Все проекты →</button>
            </div>
            <div className="divide-y">
              {projects.length === 0 ? (
                <div className="p-6 text-center text-gray-500">Нет проектов</div>
              ) : (
                projects.map((project) => (
                  <div key={project.project_id} className="p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-gray-900">{project.title}</h3>
                      <StatusBadge status={project.status} />
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span>{project.project_type}</span>
                      <HealthIndicator health={project.health} />
                    </div>
                    <div className="mt-2">
                      <ProgressBar
                        value={project.tokens_used}
                        max={project.token_budget}
                        color={
                          project.tokens_used / project.token_budget > 0.8
                            ? 'red'
                            : project.tokens_used / project.token_budget > 0.5
                            ? 'yellow'
                            : 'green'
                        }
                      />
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Tasks List */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Активные задачи</h2>
              <button className="text-sm text-blue-600 hover:text-blue-800">Все задачи →</button>
            </div>
            <div className="divide-y">
              {tasks.length === 0 ? (
                <div className="p-6 text-center text-gray-500">Нет задач</div>
              ) : (
                tasks.map((task) => (
                  <div key={task.task_id} className="p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-gray-900">{task.title}</h3>
                      <PriorityBadge priority={task.priority} />
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span className="flex items-center">
                        <Users className="w-3 h-3 mr-1" />
                        {task.assigned_agent || 'Не назначена'}
                      </span>
                      <StatusBadge status={task.status} />
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Agents Status */}
        <div className="mt-8 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">Статус агентов</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
              {agents.map((agent) => (
                <div
                  key={agent.name}
                  className="p-3 rounded-lg border bg-gray-50"
                >
                  <div className="flex items-center mb-2">
                    <span
                      className={`w-2 h-2 rounded-full mr-2 ${
                        agent.status === 'idle'
                          ? 'bg-green-500'
                          : agent.status === 'busy'
                          ? 'bg-yellow-500'
                          : 'bg-gray-400'
                      }`}
                    />
                    <span className="text-sm font-medium text-gray-900 truncate">
                      {agent.role}
                    </span>
                  </div>
                  <div className="text-xs text-gray-500">
                    {agent.status === 'idle'
                      ? 'Свободен'
                      : agent.status === 'busy'
                      ? 'Занят'
                      : 'Офлайн'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// Helper Components

function StatCard({
  title,
  value,
  total,
  critical,
  icon: Icon,
  color,
}: {
  title: string;
  value: number;
  total?: number;
  critical?: number;
  icon: React.ElementType;
  color: 'blue' | 'green' | 'red' | 'purple';
}) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    purple: 'bg-purple-100 text-purple-600',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {total !== undefined && (
            <p className="text-xs text-gray-500 mt-1">из {total}</p>
          )}
          {critical !== undefined && critical > 0 && (
            <p className="text-xs text-red-600 mt-1">{critical} критических</p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const statusConfig: Record<string, { bg: string; text: string; label: string }> = {
    planning: { bg: 'bg-gray-100', text: 'text-gray-700', label: 'Планирование' },
    active: { bg: 'bg-blue-100', text: 'text-blue-700', label: 'Активен' },
    on_hold: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: 'На паузе' },
    completed: { bg: 'bg-green-100', text: 'text-green-700', label: 'Завершен' },
    cancelled: { bg: 'bg-red-100', text: 'text-red-700', label: 'Отменен' },
    todo: { bg: 'bg-gray-100', text: 'text-gray-700', label: 'К выполнению' },
    in_progress: { bg: 'bg-blue-100', text: 'text-blue-700', label: 'В работе' },
    review: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: 'На проверке' },
    done: { bg: 'bg-green-100', text: 'text-green-700', label: 'Готово' },
    open: { bg: 'bg-red-100', text: 'text-red-700', label: 'Открыт' },
    in_progress: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: 'В работе' },
    resolved: { bg: 'bg-green-100', text: 'text-green-700', label: 'Решен' },
    closed: { bg: 'bg-gray-100', text: 'text-gray-700', label: 'Закрыт' },
  };

  const config = statusConfig[status] || { bg: 'bg-gray-100', text: 'text-gray-700', label: status };

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
      {config.label}
    </span>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const priorityConfig: Record<string, { bg: string; text: string; label: string }> = {
    low: { bg: 'bg-gray-100', text: 'text-gray-700', label: 'Низкий' },
    medium: { bg: 'bg-blue-100', text: 'text-blue-700', label: 'Средний' },
    high: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: 'Высокий' },
    critical: { bg: 'bg-red-100', text: 'text-red-700', label: 'Критический' },
  };

  const config = priorityConfig[priority] || priorityConfig.medium;

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
      {config.label}
    </span>
  );
}

function HealthIndicator({ health }: { health: string }) {
  const healthConfig: Record<string, { color: string; label: string }> = {
    green: { color: 'bg-green-500', label: 'Зеленый' },
    yellow: { color: 'bg-yellow-500', label: 'Желтый' },
    red: { color: 'bg-red-500', label: 'Красный' },
  };

  const config = healthConfig[health] || healthConfig.green;

  return (
    <span className="flex items-center">
      <span className={`w-2 h-2 rounded-full ${config.color} mr-1`} />
      <span className="text-xs">{config.label}</span>
    </span>
  );
}

function ProgressBar({
  value,
  max,
  color,
}: {
  value: number;
  max: number;
  color: 'green' | 'yellow' | 'red';
}) {
  const percentage = max > 0 ? (value / max) * 100 : 0;
  const colorClasses = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500',
  };

  return (
    <div className="w-full bg-gray-200 rounded-full h-1.5">
      <div
        className={`h-1.5 rounded-full ${colorClasses[color]} transition-all`}
        style={{ width: `${Math.min(percentage, 100)}%` }}
      />
    </div>
  );
}