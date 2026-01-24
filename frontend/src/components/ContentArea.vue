<template>
  <section class="content-area">
    <div class="content-grid">
      <Card 
        v-for="(card, index) in cards" 
        :key="card.id"
        :title="card.title"
        :description="card.description"
        :icon="card.icon"
        :status="card.status"
        :progress="card.progress"
        :index="index"
      />
    </div>
  </section>
</template>

<script setup>
import Card from './Card.vue'
import { 
  FolderKanban, 
  TrendingUp, 
  Users, 
  Lock, 
  Zap, 
  FileText 
} from 'lucide-vue-next'

const cards = [
  {
    id: 1,
    title: 'Proje Yönetimi',
    description: 'Tüm projelerinizi tek bir yerden yönetin. Ekip üyelerinizle işbirliği yapın.',
    icon: FolderKanban,
    status: 'Aktif',
    progress: 75
  },
  {
    id: 2,
    title: 'Performans Analizi',
    description: 'Detaylı raporlar ve metriklerle performansınızı takip edin.',
    icon: TrendingUp,
    status: 'Güncel',
    progress: 92
  },
  {
    id: 3,
    title: 'Ekip İşbirliği',
    description: 'Ekibinizle gerçek zamanlı olarak çalışın ve iletişim kurun.',
    icon: Users,
    status: 'Aktif',
    progress: 68
  },
  {
    id: 4,
    title: 'Güvenlik & Uyumluluk',
    description: 'Kurumsal düzeyde güvenlik ve veri koruma standartları.',
    icon: Lock,
    status: 'Korumalı',
    progress: 100
  },
  {
    id: 5,
    title: 'Otomasyon',
    description: 'İş akışlarınızı otomatikleştirin ve verimliliği artırın.',
    icon: Zap,
    status: 'Çalışıyor',
    progress: 85
  },
  {
    id: 6,
    title: 'Raporlama',
    description: 'Özelleştirilebilir raporlar ve veri görselleştirme araçları.',
    icon: FileText,
    status: 'Hazır',
    progress: 95
  }
]
</script>

<style scoped>
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  max-width: 1400px;
}
</style>
