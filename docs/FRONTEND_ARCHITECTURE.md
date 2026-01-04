# Frontend Architecture Documentation
## Sports Analytics Web Dashboard

**Version:** 2.2 (Multi-Sport Architecture + Offline-First + 3G Optimization)  
**Last Updated:** January 2025  
**Primary Market:** 🇳🇦 Namibia (Africa)  
**Currency:** N$ (Namibian Dollar)

**Related Documentation:**
- [API Documentation](API_DOCUMENTATION.md) - Backend API reference
- [Web Dashboard Quick Start](WEB_DASHBOARD_QUICKSTART.md) - Setup guide
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements
- [UI/UX Design Documentation](UI_UX_DESIGN.md) - Wireframes, layouts, and design system
- [Architecture Documentation](architecture.md) - System architecture

---

## 🇳🇦 Namibian-Specific Architecture Requirements

### Key Considerations for Namibian Market
1. **Offline-First Design** - Intermittent connectivity (53% internet penetration)
2. **Mobile-First** - 108% mobile penetration, primary access device
3. **Low-Data Optimization** - N$5-10/GB data costs
4. **3G Network Optimization** - Majority on 3G, 4G/5G limited to cities
5. **Multi-Language Support** - English (primary) + Afrikaans
6. **Local Payment Integration** - MTC Mobile Money, Bank Windhoek EFT
7. **WhatsApp/SMS Integration** - Popular communication channels
8. **Progressive Web App (PWA)** - Install without app stores

### Target Devices & Browsers (Namibian Market)
- **Mobile:** 85% of traffic
  - Android: 70% (Samsung, Huawei, affordable Chinese brands)
  - iOS: 15% (urban, higher income)
  - Feature phones: 15% (SMS notifications only)
- **Desktop:** 15% of traffic
  - Chrome: 60%
  - Firefox: 20%
  - Safari: 15%
  - Edge: 5%
- **Screen Sizes:**
  - Mobile: 360x640 to 414x896 (most common)
  - Tablet: 768x1024 (iPads at UNAM)
  - Desktop: 1366x768 to 1920x1080

### Network Conditions (Namibia)
- **3G:** 60% of connections (1-3 Mbps)
- **4G:** 35% of connections (5-20 Mbps, Windhoek/urban)
- **5G:** 5% (MTC coverage in Windhoek CBD)
- **WiFi:** Limited (UNAM campus, MTC offices, hotels)
- **Average Latency:** 150-300ms
- **Data Costs:** N$5-10 per GB

---

## 1. Technology Stack

### Core Framework
- **Next.js 14** (App Router) - React framework with SSR/SSG
- **React 18** - UI library
- **TypeScript** - Type safety

### UI & Styling
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI** - Component library for Tailwind
- **shadcn/ui** (optional) - High-quality React components
- **Framer Motion** - Animation library

### State Management
- **Zustand** - Lightweight state management
- **React Query (TanStack Query)** - Server state management
- **React Hook Form** - Form state management

### Data Visualization
- **Recharts** - Chart library
- **D3.js** - Advanced visualizations (heatmaps, networks)
- **Leaflet** - Map/field visualizations
- **react-spring** - Physics-based animations

### Video & Media
- **Video.js** or **react-player** - Video player
- **Canvas API** - Custom annotations overlay

### Utilities
- **Zod** - Schema validation
- **date-fns** - Date manipulation
- **axios** - HTTP client
- **react-router-dom** - Routing (if not using Next.js)

### Namibian-Specific Libraries & Tools
- **Workbox** - Service Worker for PWA and offline functionality
- **IndexedDB** (via Dexie.js) - Local storage for offline data
- **localForage** - Async storage (50MB+ capacity)
- **react-pwa** - PWA configuration for Next.js
- **Sharp** - Image optimization (WebP conversion)
- **react-intersection-observer** - Lazy loading (data savings)
- **react-query-offline** - Offline-first data synchronization
- **Compressor.js** - Client-side image compression
- **i18next** - Internationalization (English + Afrikaans)
- **@react-native-community/netinfo** - Network status detection
- **react-toastify** - Offline notifications

### Payment Integration (Namibian)
- **MTC Mobile Money SDK** - USSD payment integration
- **Bank Windhoek API** - EFT payment processing
- **Paygate Namibia** - Card payment gateway

### Communication (Namibian)
- **WhatsApp Business API** - Match updates, support
- **Africa's Talking SMS API** - SMS notifications (MTC, TN Mobile)
- **Twilio** - Backup SMS provider

---

## 2. Project Structure

```
dashboard/
├── public/                              # Static assets
│   ├── images/
│   │   ├── logos/                      # Team logos (16 Debmarine Premiership clubs)
│   │   │   ├── african-stars.png
│   │   │   ├── black-africa.png
│   │   │   ├── orlando-pirates.png
│   │   │   ├── civics-fc.png
│   │   │   ├── blue-waters-fc.png
│   │   │   ├── tigers-fc.png
│   │   │   ├── young-african.png
│   │   │   ├── mighty-gunners.png
│   │   │   ├── tura-magic.png
│   │   │   ├── unam-fc.png
│   │   │   ├── okahandja-united.png
│   │   │   ├── life-fighters.png
│   │   │   ├── julinho-sporting.png
│   │   │   ├── khomas-nampol.png
│   │   │   ├── citizens-fc.png
│   │   │   └── young-brazilians.png
│   │   ├── fields/                     # Field/court visualizations (8 sports)
│   │   │   ├── football-field.svg
│   │   │   ├── basketball-court.svg
│   │   │   ├── rugby-pitch.svg
│   │   │   ├── netball-court.svg
│   │   │   ├── hockey-field.svg
│   │   │   ├── cricket-pitch.svg
│   │   │   ├── tennis-court.svg
│   │   │   └── volleyball-court.svg
│   │   └── players/                    # Player photos
│   ├── icons/
│   │   ├── sports/                     # Sport icons (8 sports)
│   │   │   ├── football.svg
│   │   │   ├── basketball.svg
│   │   │   ├── rugby.svg
│   │   │   ├── netball.svg
│   │   │   ├── hockey.svg
│   │   │   ├── cricket.svg
│   │   │   ├── tennis.svg
│   │   │   └── volleyball.svg
│   │   └── ui/                         # UI icons
│   ├── fonts/                          # Custom fonts
│   ├── locales/                        # i18n translation files
│   │   ├── en/
│   │   │   ├── common.json
│   │   │   ├── matches.json
│   │   │   ├── players.json
│   │   │   ├── teams.json
│   │   │   ├── analytics.json
│   │   │   └── errors.json
│   │   ├── af/                         # Afrikaans translations
│   │   │   ├── common.json
│   │   │   ├── matches.json
│   │   │   ├── players.json
│   │   │   ├── teams.json
│   │   │   ├── analytics.json
│   │   │   └── errors.json
│   │   └── osh/                        # Oshiwambo translations (Phase 2)
│   │       ├── common.json
│   │       ├── matches.json
│   │       ├── players.json
│   │       ├── teams.json
│   │       ├── analytics.json
│   │       └── errors.json
│   ├── sw.js                           # Service worker (Workbox)
│   ├── manifest.json                   # PWA manifest
│   ├── favicon.ico
│   └── robots.txt
│
├── src/
│   ├── app/                            # Next.js App Router
│   │   ├── layout.tsx                  # Root layout
│   │   ├── page.tsx                    # Home/Dashboard page
│   │   ├── loading.tsx                 # Loading UI
│   │   ├── error.tsx                   # Error boundary
│   │   ├── not-found.tsx               # 404 page
│   │   │
│   │   ├── (auth)/                     # Authentication routes
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   └── forgot-password/
│   │   │       └── page.tsx
│   │   │
│   │   ├── matches/                    # Match routes
│   │   │   ├── page.tsx                # Match list
│   │   │   ├── [id]/
│   │   │   │   ├── page.tsx            # Match detail
│   │   │   │   ├── players/
│   │   │   │   │   └── page.tsx        # Match players
│   │   │   │   ├── teams/
│   │   │   │   │   └── page.tsx        # Match teams
│   │   │   │   └── analytics/
│   │   │   │       └── page.tsx        # Match analytics
│   │   │   └── upload/
│   │   │       └── page.tsx             # Upload match
│   │   │
│   │   ├── players/                    # Player routes
│   │   │   ├── page.tsx                # Player list
│   │   │   └── [id]/
│   │   │       └── page.tsx            # Player detail
│   │   │
│   │   ├── teams/                      # Team routes
│   │   │   ├── page.tsx                # Team list
│   │   │   └── [id]/
│   │   │       └── page.tsx            # Team detail
│   │   │
│   │   ├── tournaments/                # Tournament routes
│   │   │   ├── page.tsx                # Tournament list
│   │   │   └── [id]/
│   │   │       └── page.tsx            # Tournament detail (MTC Maris Cup)
│   │   │
│   │   ├── analytics/                  # Analytics routes
│   │   │   ├── page.tsx                # Analytics dashboard
│   │   │   ├── scouting/
│   │   │   │   └── page.tsx            # Scouting dashboard
│   │   │   └── comparisons/
│   │   │       └── page.tsx            # Team/player comparisons
│   │   │
│   │   ├── settings/                   # Settings routes
│   │   │   ├── page.tsx                # User settings
│   │   │   ├── profile/
│   │   │   │   └── page.tsx
│   │   │   ├── notifications/
│   │   │   │   └── page.tsx
│   │   │   └── billing/
│   │   │       └── page.tsx
│   │   │
│   │   └── api/                        # API routes (Next.js)
│   │       ├── auth/
│   │       │   ├── login/
│   │       │   │   └── route.ts
│   │       │   ├── register/
│   │       │   │   └── route.ts
│   │       │   ├── logout/
│   │       │   │   └── route.ts
│   │       │   ├── refresh/
│   │       │   │   └── route.ts
│   │       │   └── verify/
│   │       │       └── route.ts        # Email verification
│   │       ├── webhooks/
│   │       │   ├── payments/
│   │       │   │   └── route.ts        # MTC Mobile Money webhooks
│   │       │   ├── whatsapp/
│   │       │   │   └── route.ts        # WhatsApp Business API webhooks
│   │       │   └── sms/
│   │       │       └── route.ts        # SMS delivery status webhooks
│   │       ├── upload/
│   │       │   └── route.ts            # File upload endpoint
│   │       ├── sync/
│   │       │   └── route.ts            # Offline data sync endpoint
│   │       └── health/
│   │           └── route.ts            # Health check endpoint
│   │
│   ├── components/
│   │   ├── ui/                         # Base UI components (shadcn/ui)
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Table.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Dialog.tsx
│   │   │   ├── Dropdown.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Checkbox.tsx
│   │   │   ├── Radio.tsx
│   │   │   ├── Tabs.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Avatar.tsx
│   │   │   ├── Skeleton.tsx
│   │   │   ├── Toast.tsx
│   │   │   ├── Tooltip.tsx
│   │   │   ├── Progress.tsx
│   │   │   ├── Spinner.tsx
│   │   │   ├── Alert.tsx
│   │   │   ├── Accordion.tsx
│   │   │   ├── Breadcrumb.tsx
│   │   │   ├── Pagination.tsx
│   │   │   ├── Switch.tsx
│   │   │   ├── Slider.tsx
│   │   │   ├── Textarea.tsx
│   │   │   ├── Label.tsx
│   │   │   ├── Separator.tsx
│   │   │   ├── Sheet.tsx
│   │   │   ├── Popover.tsx
│   │   │   ├── Command.tsx
│   │   │   ├── Calendar.tsx
│   │   │   ├── DatePicker.tsx
│   │   │   ├── TimePicker.tsx
│   │   │   └── FileUpload.tsx
│   │   │
│   │   ├── layout/                     # Layout components
│   │   │   ├── Header.tsx
│   │   │   │   ├── Logo.tsx
│   │   │   │   ├── Navigation.tsx
│   │   │   │   ├── Search.tsx
│   │   │   │   ├── UserMenu.tsx
│   │   │   │   ├── LanguageSwitcher.tsx
│   │   │   │   └── SportSwitcher.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   │   ├── NavItem.tsx
│   │   │   │   └── NavSection.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── OfflineIndicator.tsx
│   │   │   └── NetworkStatus.tsx
│   │   │
│   │   ├── universal/                  # 13 Universal Multi-Sport Components
│   │   │   ├── MatchCard.tsx           # Universal match display
│   │   │   ├── PlayingAreaVisualization.tsx  # Field/court/pitch renderer
│   │   │   ├── StatCard.tsx            # Metric display for any sport
│   │   │   ├── ParticipantCard.tsx     # Player/team information
│   │   │   ├── EventTimeline.tsx       # Match events chronologically
│   │   │   ├── ScoreDisplay.tsx        # Sport-appropriate score formatting
│   │   │   ├── PerformanceChart.tsx     # Universal metric visualization
│   │   │   ├── LeagueTable.tsx          # Standings for any competition
│   │   │   ├── ComparisonView.tsx      # Side-by-side analysis
│   │   │   ├── FilterPanel.tsx          # Universal filtering system
│   │   │   ├── TournamentBracket.tsx    # Tournament bracket visualization
│   │   │   ├── SportAdapter.tsx         # Data transformation wrapper
│   │   │   └── SportSelector.tsx        # Sport switching component
│   │   │
│   │   ├── analytics/                  # Analytics-specific components
│   │   │   ├── Heatmap.tsx             # Player heatmap visualization
│   │   │   ├── PassNetwork.tsx         # Pass network graph
│   │   │   ├── PlayerCard.tsx          # Player statistics card
│   │   │   ├── StatsCard.tsx           # Statistics display card
│   │   │   ├── VideoPlayer.tsx         # Video player with annotations
│   │   │   ├── Timeline.tsx            # Event timeline
│   │   │   ├── PositionMap.tsx          # Position visualization
│   │   │   ├── SpeedChart.tsx          # Speed/distance charts
│   │   │   ├── PossessionChart.tsx     # Possession visualization
│   │   │   ├── FormationView.tsx       # Team formation display
│   │   │   ├── ZoneAnalysis.tsx        # Zone-based analysis
│   │   │   ├── ShotMap.tsx             # Shot location map
│   │   │   ├── PressureMap.tsx         # Defensive pressure visualization
│   │   │   └── TacticalView.tsx        # Tactical analysis view
│   │   │
│   │   ├── forms/                      # Form components
│   │   │   ├── UploadForm.tsx          # Match video upload
│   │   │   ├── FilterForm.tsx          # Data filtering
│   │   │   ├── SearchForm.tsx          # Search functionality
│   │   │   ├── MatchMetadataForm.tsx   # Match metadata input
│   │   │   └── SettingsForm.tsx        # Settings forms
│   │   │
│   │   ├── charts/                     # Chart components (Recharts)
│   │   │   ├── LineChart.tsx
│   │   │   ├── BarChart.tsx
│   │   │   ├── PieChart.tsx
│   │   │   ├── AreaChart.tsx
│   │   │   └── RadarChart.tsx
│   │   │
│   │   └── providers/                   # Context providers
│   │       ├── SportProvider.tsx      # Sport context (multi-sport)
│   │       ├── ThemeProvider.tsx       # Theme context
│   │       ├── QueryProvider.tsx       # React Query provider
│   │       ├── AuthProvider.tsx        # Authentication context
│   │       └── OfflineProvider.tsx     # Offline status context
│   │
│   ├── adapters/                       # Sport Adapter Pattern
│   │   ├── ISportAdapter.ts            # Adapter interface
│   │   ├── SportAdapterFactory.ts      # Adapter factory
│   │   ├── FootballAdapter.ts          # Football adapter
│   │   ├── BasketballAdapter.ts        # Basketball adapter
│   │   ├── RugbyAdapter.ts             # Rugby adapter
│   │   ├── NetballAdapter.ts           # Netball adapter
│   │   ├── HockeyAdapter.ts            # Field hockey adapter
│   │   ├── CricketAdapter.ts            # Cricket adapter
│   │   ├── TennisAdapter.ts            # Tennis adapter
│   │   └── VolleyballAdapter.ts         # Volleyball adapter
│   │
│   ├── config/                         # Configuration files
│   │   ├── sports/                     # Sport configurations
│   │   │   ├── football.config.ts      # Football SportConfig
│   │   │   ├── basketball.config.ts   # Basketball SportConfig
│   │   │   ├── rugby.config.ts        # Rugby SportConfig
│   │   │   ├── netball.config.ts      # Netball SportConfig
│   │   │   ├── hockey.config.ts       # Hockey SportConfig
│   │   │   ├── cricket.config.ts      # Cricket SportConfig
│   │   │   ├── tennis.config.ts       # Tennis SportConfig
│   │   │   ├── volleyball.config.ts   # Volleyball SportConfig
│   │   │   └── index.ts               # Export all configs
│   │   ├── i18n.ts                    # i18next configuration
│   │   ├── pwa.ts                     # PWA configuration
│   │   └── constants.ts                # App constants
│   │
│   ├── contexts/                       # React contexts
│   │   ├── SportContext.tsx           # Sport selection context
│   │   ├── AuthContext.tsx            # Authentication context
│   │   ├── ThemeContext.tsx           # Theme context
│   │   └── OfflineContext.tsx         # Offline status context
│   │
│   ├── hooks/                          # Custom React hooks
│   │   ├── data/                      # Data fetching hooks
│   │   │   ├── useMatch.ts            # Match data hook
│   │   │   ├── usePlayer.ts           # Player data hook
│   │   │   ├── useTeam.ts             # Team data hook
│   │   │   ├── useTournament.ts       # Tournament data hook
│   │   │   ├── useAnalytics.ts        # Analytics data hook
│   │   │   └── useOfflineMatch.ts     # Offline match hook
│   │   ├── network/                   # Network hooks
│   │   │   ├── useWebSocket.ts        # WebSocket hook
│   │   │   ├── useNetworkStatus.ts    # Network status hook
│   │   │   └── useOnlineSync.ts       # Online sync hook
│   │   ├── sport/                     # Sport-specific hooks
│   │   │   ├── useSport.ts            # Sport context hook
│   │   │   ├── useSportAdapter.ts     # Sport adapter hook
│   │   │   └── useSportConfig.ts      # Sport config hook
│   │   ├── ui/                        # UI hooks
│   │   │   ├── useModal.ts            # Modal state hook
│   │   │   ├── useToast.ts            # Toast notification hook
│   │   │   ├── useDebounce.ts         # Debounce hook
│   │   │   └── useIntersection.ts     # Intersection observer hook
│   │   └── optimization/               # Optimization hooks
│   │       ├── useProgressiveMatch.ts # Progressive loading hook
│   │       ├── useLazyLoad.ts         # Lazy loading hook
│   │       └── useRequestBatch.ts     # Request batching hook
│   │
│   ├── services/                       # API services
│   │   ├── api.ts                     # Base API client (axios)
│   │   ├── matches.ts                 # Match API service
│   │   ├── players.ts                 # Player API service
│   │   ├── teams.ts                   # Team API service
│   │   ├── tournaments.ts             # Tournament API service
│   │   ├── analytics.ts               # Analytics API service
│   │   ├── auth.ts                    # Authentication service
│   │   ├── upload.ts                  # File upload service
│   │   ├── payments.ts                # Payment service (MTC Mobile Money)
│   │   ├── notifications.ts           # Notification service (WhatsApp/SMS)
│   │   ├── scouting.ts                # Scouting service
│   │   ├── export.ts                  # Data export service
│   │   └── sync.ts                    # Offline sync service
│   │
│   ├── store/                          # State management (Zustand)
│   │   ├── useAuthStore.ts            # Authentication store
│   │   ├── useMatchStore.ts           # Match store
│   │   ├── usePlayerStore.ts          # Player store
│   │   ├── useTeamStore.ts            # Team store
│   │   ├── useUIStore.ts              # UI state store
│   │   ├── useSportStore.ts           # Sport selection store
│   │   └── useOfflineStore.ts         # Offline data store
│   │
│   ├── lib/                            # Library configurations
│   │   ├── db.ts                      # IndexedDB (Dexie.js)
│   │   ├── axios.ts                   # Axios configuration
│   │   ├── queryClient.ts             # React Query client
│   │   ├── websocket.ts               # WebSocket client
│   │   ├── compression.ts             # Data compression (pako)
│   │   ├── imageCompression.ts        # Image compression (Compressor.js)
│   │   └── requestBatcher.ts          # Request batching utility
│   │
│   ├── utils/                          # Utility functions
│   │   ├── formatters/                 # Data formatting
│   │   │   ├── formatDate.ts
│   │   │   ├── formatCurrency.ts
│   │   │   ├── formatTime.ts
│   │   │   ├── formatNumber.ts
│   │   │   ├── formatScore.ts
│   │   │   ├── formatMetric.ts
│   │   │   └── index.ts
│   │   ├── validators/                 # Data validation (Zod)
│   │   │   ├── matchValidator.ts
│   │   │   ├── playerValidator.ts
│   │   │   ├── teamValidator.ts
│   │   │   ├── tournamentValidator.ts
│   │   │   ├── uploadValidator.ts
│   │   │   ├── authValidator.ts
│   │   │   └── index.ts
│   │   ├── constants/                 # App constants
│   │   │   ├── sports.ts              # Sport constants
│   │   │   ├── teams.ts               # Team constants (Namibian - 16 clubs)
│   │   │   ├── routes.ts              # Route constants
│   │   │   ├── api.ts                 # API endpoint constants
│   │   │   ├── events.ts              # Event type constants
│   │   │   ├── metrics.ts             # Metric constants
│   │   │   ├── positions.ts           # Position constants
│   │   │   └── index.ts
│   │   ├── helpers/                   # Helper functions
│   │   │   ├── debounce.ts
│   │   │   ├── throttle.ts
│   │   │   ├── classNames.ts
│   │   │   ├── arrayHelpers.ts
│   │   │   ├── objectHelpers.ts
│   │   │   ├── stringHelpers.ts
│   │   │   ├── dateHelpers.ts
│   │   │   ├── numberHelpers.ts
│   │   │   ├── storageHelpers.ts
│   │   │   ├── urlHelpers.ts
│   │   │   ├── errorHelpers.ts
│   │   │   └── asyncHelpers.ts
│   │   └── namibian/                  # Namibian-specific utilities
│   │       ├── currency.ts            # N$ formatting
│   │       ├── teams.ts               # Namibian team helpers
│   │       └── localization.ts         # Localization helpers
│   │
│   ├── types/                          # TypeScript type definitions
│   │   ├── sport.ts                   # Sport types (SportConfig, etc.)
│   │   ├── adapter.ts                 # Adapter types (ISportAdapter)
│   │   ├── match.ts                   # Match types
│   │   ├── player.ts                  # Player types
│   │   ├── team.ts                    # Team types
│   │   ├── tournament.ts             # Tournament types
│   │   ├── analytics.ts              # Analytics types
│   │   ├── api.ts                    # API types
│   │   ├── auth.ts                   # Authentication types
│   │   ├── ui.ts                     # UI component types
│   │   └── universal.ts               # Universal component types
│   │
│   ├── styles/                         # Global styles
│   │   ├── globals.css                # Global CSS
│   │   ├── tailwind.css               # Tailwind imports
│   │   └── variables.css              # CSS variables
│   │
│   └── middleware.ts                   # Next.js middleware (auth, etc.)
│
├── tests/                              # Test files
│   ├── components/
│   │   ├── universal/                 # Universal component tests (13 components)
│   │   │   ├── MatchCard.test.tsx
│   │   │   ├── PlayingAreaVisualization.test.tsx
│   │   │   ├── StatCard.test.tsx
│   │   │   ├── ParticipantCard.test.tsx
│   │   │   ├── EventTimeline.test.tsx
│   │   │   ├── ScoreDisplay.test.tsx
│   │   │   ├── PerformanceChart.test.tsx
│   │   │   ├── LeagueTable.test.tsx
│   │   │   ├── ComparisonView.test.tsx
│   │   │   ├── FilterPanel.test.tsx
│   │   │   ├── TournamentBracket.test.tsx
│   │   │   ├── SportAdapter.test.tsx
│   │   │   └── SportSelector.test.tsx
│   │   ├── analytics/                 # Analytics component tests
│   │   │   ├── Heatmap.test.tsx
│   │   │   ├── PassNetwork.test.tsx
│   │   │   ├── PlayerCard.test.tsx
│   │   │   ├── StatsCard.test.tsx
│   │   │   ├── VideoPlayer.test.tsx
│   │   │   ├── Timeline.test.tsx
│   │   │   ├── PositionMap.test.tsx
│   │   │   ├── SpeedChart.test.tsx
│   │   │   ├── PossessionChart.test.tsx
│   │   │   └── FormationView.test.tsx
│   │   ├── ui/                        # UI component tests
│   │   │   ├── Button.test.tsx
│   │   │   ├── Card.test.tsx
│   │   │   ├── Table.test.tsx
│   │   │   ├── Modal.test.tsx
│   │   │   ├── Dialog.test.tsx
│   │   │   ├── Input.test.tsx
│   │   │   ├── Select.test.tsx
│   │   │   ├── Checkbox.test.tsx
│   │   │   ├── Radio.test.tsx
│   │   │   ├── Tabs.test.tsx
│   │   │   ├── Badge.test.tsx
│   │   │   ├── Avatar.test.tsx
│   │   │   ├── Skeleton.test.tsx
│   │   │   ├── Toast.test.tsx
│   │   │   ├── Tooltip.test.tsx
│   │   │   └── Progress.test.tsx
│   │   ├── layout/                    # Layout component tests
│   │   │   ├── Header.test.tsx
│   │   │   ├── Sidebar.test.tsx
│   │   │   └── Footer.test.tsx
│   │   ├── forms/                     # Form component tests
│   │   │   ├── UploadForm.test.tsx
│   │   │   ├── FilterForm.test.tsx
│   │   │   ├── SearchForm.test.tsx
│   │   │   ├── MatchMetadataForm.test.tsx
│   │   │   └── SettingsForm.test.tsx
│   │   └── charts/                    # Chart component tests
│   │       ├── LineChart.test.tsx
│   │       ├── BarChart.test.tsx
│   │       ├── PieChart.test.tsx
│   │       └── RadarChart.test.tsx
│   ├── hooks/
│   │   ├── data/
│   │   │   ├── useMatch.test.ts
│   │   │   ├── usePlayer.test.ts
│   │   │   ├── useTeam.test.ts
│   │   │   ├── useTournament.test.ts
│   │   │   ├── useAnalytics.test.ts
│   │   │   └── useOfflineMatch.test.ts
│   │   ├── network/
│   │   │   ├── useWebSocket.test.ts
│   │   │   ├── useNetworkStatus.test.ts
│   │   │   └── useOnlineSync.test.ts
│   │   ├── sport/
│   │   │   ├── useSport.test.ts
│   │   │   ├── useSportAdapter.test.ts
│   │   │   └── useSportConfig.test.ts
│   │   ├── ui/
│   │   │   ├── useModal.test.ts
│   │   │   ├── useToast.test.ts
│   │   │   ├── useDebounce.test.ts
│   │   │   └── useIntersection.test.ts
│   │   └── optimization/
│   │       ├── useProgressiveMatch.test.ts
│   │       ├── useLazyLoad.test.ts
│   │       └── useRequestBatch.test.ts
│   ├── adapters/
│   │   ├── ISportAdapter.test.ts
│   │   ├── SportAdapterFactory.test.ts
│   │   ├── FootballAdapter.test.ts
│   │   ├── BasketballAdapter.test.ts
│   │   ├── RugbyAdapter.test.ts
│   │   ├── NetballAdapter.test.ts
│   │   ├── HockeyAdapter.test.ts
│   │   ├── CricketAdapter.test.ts
│   │   ├── TennisAdapter.test.ts
│   │   └── VolleyballAdapter.test.ts
│   ├── services/
│   │   ├── api.test.ts
│   │   ├── matches.test.ts
│   │   ├── players.test.ts
│   │   ├── teams.test.ts
│   │   ├── tournaments.test.ts
│   │   ├── analytics.test.ts
│   │   ├── auth.test.ts
│   │   ├── upload.test.ts
│   │   ├── payments.test.ts
│   │   └── notifications.test.ts
│   ├── utils/
│   │   ├── formatters/
│   │   │   ├── formatDate.test.ts
│   │   │   ├── formatCurrency.test.ts
│   │   │   ├── formatTime.test.ts
│   │   │   └── formatNumber.test.ts
│   │   ├── validators/
│   │   │   ├── matchValidator.test.ts
│   │   │   ├── playerValidator.test.ts
│   │   │   └── uploadValidator.test.ts
│   │   ├── helpers/
│   │   │   ├── debounce.test.ts
│   │   │   ├── throttle.test.ts
│   │   │   └── classNames.test.ts
│   │   └── namibian/
│   │       ├── currency.test.ts
│   │       ├── teams.test.ts
│   │       └── localization.test.ts
│   ├── __mocks__/                     # Test mocks
│   │   ├── api.ts                     # API client mock
│   │   ├── db.ts                      # IndexedDB mock
│   │   ├── websocket.ts               # WebSocket mock
│   │   ├── matchData.ts               # Sample match data
│   │   ├── playerData.ts              # Sample player data
│   │   ├── teamData.ts                # Sample team data
│   │   ├── sportConfigs.ts            # Sport config mocks
│   │   └── adapters.ts                # Adapter mocks
│   └── setup.ts                       # Test setup
│
├── .env.local                          # Local environment variables
├── .env.production                    # Production environment variables
├── .env.development                   # Development environment variables
├── .env.example                       # Environment variables template
├── .gitignore
├── .editorconfig                     # Editor configuration
├── package.json
├── package-lock.json
├── tsconfig.json                      # TypeScript configuration
├── tsconfig.test.json                 # Test TypeScript config
├── tailwind.config.js                 # Tailwind CSS configuration
├── next.config.js                     # Next.js configuration
├── next-env.d.ts                      # Next.js TypeScript declarations
├── jest.config.js                     # Jest configuration
├── jest.setup.ts                      # Jest test setup
├── .eslintrc.json                     # ESLint configuration
├── .prettierrc                        # Prettier configuration
├── .prettierignore                    # Prettier ignore patterns
├── .husky/                            # Git hooks (Husky)
│   ├── pre-commit                    # Pre-commit hook
│   └── commit-msg                     # Commit message hook
├── .vscode/                           # VS Code settings (optional)
│   ├── settings.json
│   └── extensions.json
├── public/
│   └── sw.js                          # Service worker (generated by Workbox)
├── workbox-config.js                  # Workbox configuration
├── postcss.config.js                  # PostCSS configuration
├── .babelrc                           # Babel configuration (if needed)
├── .nvmrc                             # Node version (optional)
├── docker-compose.yml                 # Docker compose (optional)
├── Dockerfile                         # Dockerfile (optional)
├── CHANGELOG.md                       # Changelog
├── CONTRIBUTING.md                    # Contribution guidelines
├── LICENSE                            # License file
└── README.md                          # Project README
```

### 2.1 Project Structure Summary

**Total Files & Directories:**
- **Components:** 80+ components (13 universal + 10+ analytics + 30+ UI + forms + charts + layout)
- **Hooks:** 20+ custom hooks (data, network, sport, ui, optimization)
- **Services:** 11 API services (matches, players, teams, tournaments, analytics, auth, upload, payments, notifications, scouting, export, sync)
- **Adapters:** 8 sport adapters (Football, Basketball, Rugby, Netball, Hockey, Cricket, Tennis, Volleyball)
- **Configs:** 8 sport configs + i18n + PWA + constants
- **Stores:** 10 Zustand stores (auth, match, player, team, tournament, analytics, UI, sport, offline, notification)
- **Types:** 15+ TypeScript type definition files
- **Utils:** 30+ utility functions (formatters, validators, helpers, Namibian-specific)
- **Tests:** 100+ test files covering all components, hooks, adapters, services, and utils
- **Routes:** 25+ Next.js App Router pages
- **API Routes:** 10+ API route handlers

**Key Statistics:**
- **Multi-Sport Support:** 8 sports fully configured
- **Namibian Teams:** 16 Debmarine Premiership clubs
- **Languages:** 3 languages (English, Afrikaans, Oshiwambo)
- **Universal Components:** 13 sport-agnostic components
- **Offline-First:** Complete PWA with service worker and IndexedDB
- **3G Optimization:** Compression, lazy loading, progressive loading

### 2.2 Key Directory Explanations

#### **Multi-Sport Architecture Files**

**`src/adapters/`** - Sport Adapter Pattern
- Implements `ISportAdapter` interface for each sport
- Transforms sport-specific data into universal format
- Factory pattern for adapter retrieval
- **8 adapters** for Namibian priority sports

**`src/config/sports/`** - Sport Configuration System
- `SportConfig` objects defining sport rules, dimensions, scoring
- One config file per sport (8 sports configured)
- **Zero code changes** needed to add new sports

**`src/components/universal/`** - 13 Universal Components
- Sport-agnostic components working across all sports
- Driven by `SportConfig` and adapters
- Includes: MatchCard, PlayingAreaVisualization, StatCard, etc.

**`src/contexts/SportContext.tsx`** - Global Sport State
- Manages current sport selection
- Provides adapter and config to all components
- Enables sport switching without page reload

#### **Offline-First Implementation**

**`public/sw.js`** - Service Worker (Workbox)
- Caches static assets and API responses
- Background sync for offline actions
- Network-first strategy with cache fallback

**`src/lib/db.ts`** - IndexedDB (Dexie.js)
- Offline data storage (matches, players, teams)
- Sync queue for offline actions
- 50MB+ storage capacity

**`src/hooks/network/`** - Network Hooks
- `useNetworkStatus` - Real-time connection monitoring
- `useOnlineSync` - Automatic sync when online
- `useOfflineMatch` - Offline-first data fetching

#### **Localization (i18n)**

**`public/locales/`** - Translation Files
- `en/` - English (baseline, complete)
- `af/` - Afrikaans (11% of population, complete)
- `osh/` - Oshiwambo (49% of population, Phase 2)

**`src/config/i18n.ts`** - i18next Configuration
- Language detection (localStorage, navigator)
- Fallback to English
- Dynamic translation loading

#### **Namibian-Specific Files**

**`src/utils/namibian/`** - Namibian Utilities
- Currency formatting (N$)
- Team helpers (16 Debmarine Premiership clubs)
- Localization helpers

**`src/services/payments.ts`** - Payment Integration
- MTC Mobile Money SDK
- Bank Windhoek EFT
- Paygate Namibia (card payments)

**`src/services/notifications.ts`** - Communication
- WhatsApp Business API
- Africa's Talking SMS API
- Twilio (backup SMS)

#### **3G Network Optimization**

**`src/lib/compression.ts`** - Data Compression
- Gzip compression for API responses
- Reduces payload size by 60-80%

**`src/lib/imageCompression.ts`** - Image Optimization
- Client-side compression before upload
- Quality reduction on 3G networks
- WebP conversion

**`src/lib/requestBatcher.ts`** - Request Batching
- Batches multiple requests within 100ms
- Reduces network overhead

**`src/hooks/optimization/`** - Optimization Hooks
- Progressive data loading (critical first)
- Lazy loading with intersection observer
- Request batching

#### **Component Organization**

**`src/components/ui/`** - Base Components
- Reusable UI primitives (Button, Card, Modal, etc.)
- Based on shadcn/ui or DaisyUI
- Accessible and themeable

**`src/components/universal/`** - Multi-Sport Components
- 13 universal components working across all sports
- Sport-agnostic design
- Driven by adapters and configs

**`src/components/analytics/`** - Analytics Components
- Sport-specific visualizations (heatmaps, networks)
- Video player with annotations
- Advanced statistics displays

#### **State Management**

**`src/store/`** - Zustand Stores
- Lightweight state management
- Separate stores for different domains
- Offline store for sync queue

**`src/contexts/`** - React Contexts
- Global state (sport, auth, theme, offline)
- Provider pattern for app-wide access

#### **Type Safety**

**`src/types/`** - TypeScript Definitions
- Complete type coverage
- Sport types (SportConfig, ISportAdapter)
- Universal component types
- API response types

#### **Testing Structure**

**`tests/`** - Comprehensive Test Suite
- Component tests (universal, analytics, UI)
- Hook tests
- Adapter tests (sport-specific)
- Service tests
- Utility tests

### 2.2 File Naming Conventions

- **Components:** PascalCase (e.g., `MatchCard.tsx`)
- **Hooks:** camelCase with `use` prefix (e.g., `useMatch.ts`)
- **Services:** camelCase (e.g., `matches.ts`)
- **Types:** camelCase (e.g., `match.ts`)
- **Utils:** camelCase (e.g., `formatters.ts`)
- **Configs:** camelCase with `.config.ts` suffix (e.g., `football.config.ts`)
- **Adapters:** PascalCase with `Adapter` suffix (e.g., `FootballAdapter.ts`)

### 2.3 Import Path Aliases

```typescript
// tsconfig.json paths
{
  "@/*": ["./src/*"],
  "@/components/*": ["./src/components/*"],
  "@/hooks/*": ["./src/hooks/*"],
  "@/services/*": ["./src/services/*"],
  "@/adapters/*": ["./src/adapters/*"],
  "@/config/*": ["./src/config/*"],
  "@/types/*": ["./src/types/*"],
  "@/utils/*": ["./src/utils/*"],
  "@/lib/*": ["./src/lib/*"]
}

// Usage
import { MatchCard } from '@/components/universal/MatchCard';
import { useMatch } from '@/hooks/data/useMatch';
import { FootballAdapter } from '@/adapters/FootballAdapter';
```

---

## 3. Component Architecture

### 3.1 Component Hierarchy

```
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   ├── Search
│   │   └── UserMenu
│   ├── Sidebar
│   │   ├── NavItem (Matches)
│   │   ├── NavItem (Players)
│   │   ├── NavItem (Teams)
│   │   └── NavItem (Analytics)
│   └── MainContent
│       └── [Page Components]
│           ├── MatchListPage
│           │   ├── MatchTable
│           │   └── MatchFilters
│           ├── MatchDetailPage
│           │   ├── MatchHeader
│           │   ├── MatchTabs
│           │   │   ├── OverviewTab
│           │   │   ├── PlayersTab
│           │   │   ├── TeamsTab
│           │   │   └── AnalyticsTab
│           │   └── VideoPlayer
│           └── PlayerDetailPage
│               ├── PlayerCard
│               ├── StatsCards
│               ├── Heatmap
│               └── PassNetwork
```

### 3.2 Component Patterns

#### Container/Presentational Pattern
```typescript
// Container (Smart Component)
const MatchListContainer = () => {
  const { data, isLoading } = useQuery(['matches'], fetchMatches);
  return <MatchList data={data} loading={isLoading} />;
};

// Presentational (Dumb Component)
const MatchList = ({ data, loading }) => {
  if (loading) return <Loading />;
  return <Table data={data} />;
};
```

#### Custom Hooks Pattern
```typescript
// useMatch.ts
export const useMatch = (matchId: string) => {
  const query = useQuery(
    ['match', matchId],
    () => api.matches.getById(matchId),
    { enabled: !!matchId }
  );
  
  return {
    match: query.data,
    isLoading: query.isLoading,
    error: query.error,
    refetch: query.refetch
  };
};
```

---

## 4. State Management

### 4.1 Server State (React Query)

```typescript
// queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});
```

### 4.2 Client State (Zustand)

```typescript
// useUIStore.ts
import create from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'light',
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));
```

---

## 5. API Integration

### 5.1 API Client Setup

```typescript
// services/api.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 5.2 Service Layer

```typescript
// services/matches.ts
import apiClient from './api';

export const matchesService = {
  list: (params?: MatchListParams) =>
    apiClient.get('/matches', { params }),
  
  getById: (id: string) =>
    apiClient.get(`/matches/${id}`),
  
  upload: (file: File, metadata: MatchMetadata) => {
    const formData = new FormData();
    formData.append('file', file);
    Object.entries(metadata).forEach(([key, value]) => {
      formData.append(key, value);
    });
    return apiClient.post('/matches', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  delete: (id: string) =>
    apiClient.delete(`/matches/${id}`),
  
  getStatus: (id: string) =>
    apiClient.get(`/matches/${id}/status`),
};
```

---

## 6. Key Components

### 6.1 Match Table Component

```typescript
// components/analytics/MatchTable.tsx
import { useQuery } from '@tanstack/react-query';
import { matchesService } from '@/services/matches';

export const MatchTable = () => {
  const { data, isLoading } = useQuery(
    ['matches'],
    () => matchesService.list()
  );
  
  return (
    <div className="overflow-x-auto">
      <table className="table w-full">
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Teams</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data?.matches.map((match) => (
            <MatchTableRow key={match.id} match={match} />
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### 6.2 Heatmap Component

```typescript
// components/analytics/Heatmap.tsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface HeatmapProps {
  data: HeatmapData;
  width?: number;
  height?: number;
}

export const Heatmap = ({ data, width = 1050, height = 680 }: HeatmapProps) => {
  const svgRef = useRef<SVGSVGElement>(null);
  
  useEffect(() => {
    if (!svgRef.current) return;
    
    // D3.js heatmap rendering
    const svg = d3.select(svgRef.current);
    // ... heatmap implementation
    
  }, [data]);
  
  return (
    <div className="heatmap-container">
      <svg ref={svgRef} width={width} height={height} />
    </div>
  );
};
```

### 6.3 Video Player Component

```typescript
// components/analytics/VideoPlayer.tsx
import { useRef, useEffect } from 'react';
import videojs from 'video.js';

interface VideoPlayerProps {
  src: string;
  annotations?: Annotation[];
  onEventClick?: (event: Event) => void;
}

export const VideoPlayer = ({ src, annotations, onEventClick }: VideoPlayerProps) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<any>(null);
  
  useEffect(() => {
    if (videoRef.current && !playerRef.current) {
      playerRef.current = videojs(videoRef.current, {
        controls: true,
        responsive: true,
      });
    }
    
    return () => {
      if (playerRef.current) {
        playerRef.current.dispose();
      }
    };
  }, []);
  
  return (
    <div className="video-player-wrapper">
      <video ref={videoRef} className="video-js" />
      <CanvasOverlay annotations={annotations} />
    </div>
  );
};
```

---

## 7. Routing

### 7.1 Next.js App Router

```typescript
// app/matches/[id]/page.tsx
export default function MatchDetailPage({ params }: { params: { id: string } }) {
  const { match, isLoading } = useMatch(params.id);
  
  if (isLoading) return <Loading />;
  if (!match) return <NotFound />;
  
  return (
    <div>
      <MatchHeader match={match} />
      <MatchTabs matchId={params.id} />
    </div>
  );
}
```

### 7.2 Route Structure

```
/                          # Home/Dashboard
/matches                   # Match list
/matches/[id]              # Match detail
/matches/[id]/players      # Players in match
/matches/[id]/players/[playerId]  # Player detail
/matches/[id]/teams        # Teams in match
/matches/[id]/teams/[teamId]       # Team detail
/matches/[id]/analytics    # Analytics overview
/upload                    # Upload match
/settings                  # User settings
/login                     # Authentication
```

---

## 8. Performance Optimization

### 8.1 Code Splitting

```typescript
// Lazy load heavy components
const Heatmap = lazy(() => import('@/components/analytics/Heatmap'));
const PassNetwork = lazy(() => import('@/components/analytics/PassNetwork'));

// Use Suspense
<Suspense fallback={<Loading />}>
  <Heatmap data={heatmapData} />
</Suspense>
```

### 8.2 Image Optimization

```typescript
// Next.js Image component
import Image from 'next/image';

<Image
  src="/heatmap.png"
  alt="Player heatmap"
  width={1050}
  height={680}
  priority
/>
```

### 8.3 Memoization

```typescript
// Memoize expensive computations
const processedData = useMemo(
  () => processHeatmapData(rawData),
  [rawData]
);

// Memoize components
const PlayerCard = memo(({ player }: { player: Player }) => {
  // ...
});
```

---

## 9. Testing Strategy

### 9.1 Unit Tests

```typescript
// tests/components/PlayerCard.test.tsx
import { render, screen } from '@testing-library/react';
import { PlayerCard } from '@/components/analytics/PlayerCard';

describe('PlayerCard', () => {
  it('renders player information', () => {
    const player = { jersey_number: 10, team: 1 };
    render(<PlayerCard player={player} />);
    expect(screen.getByText('10')).toBeInTheDocument();
  });
});
```

### 9.2 Integration Tests

```typescript
// tests/pages/MatchDetailPage.test.tsx
import { render, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MatchDetailPage from '@/pages/MatchDetailPage';

test('loads and displays match data', async () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <MatchDetailPage matchId="123" />
    </QueryClientProvider>
  );
  
  await waitFor(() => {
    expect(screen.getByText('Team A vs Team B')).toBeInTheDocument();
  });
});
```

---

## 10. Basic Deployment Configuration

### 10.1 Development Build Configuration

```javascript
// next.config.js (Development)
module.exports = {
  output: 'standalone',
  images: {
    domains: ['api.sportsanalytics.na', 'localhost'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};
```

### 10.2 Environment Variables

```bash
# .env.local (Development)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

**Note:** For production deployment configuration, see [Section 18: Deployment & Production](#18-deployment--production).

---

## 11. Accessibility

### 11.1 ARIA Labels

```typescript
<button
  aria-label="Upload match video"
  onClick={handleUpload}
>
  Upload
</button>
```

### 11.2 Keyboard Navigation

```typescript
// Ensure all interactive elements are keyboard accessible
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Clickable element
</div>
```

---

## 12. Localization & Internationalization

### 12.1 Namibian Language Strategy

**Linguistic Landscape:**

Namibia has **13 recognized national languages** with English as the official language:

| Language | Speakers | % Population | Priority | Timeline |
|----------|----------|--------------|----------|----------|
| **English** | 70% (understood) | Official | Phase 1 | ✅ Launch |
| **Afrikaans** | 286,000 | 11% | Phase 1 | ✅ Launch |
| **Oshiwambo** | 1,280,000 | 49% | Phase 2 | Month 6-9 |
| **Otjiherero** | 234,000 | 9% | Phase 3 | Year 2 |
| **RuKavango** | 234,000 | 9% | Phase 4 | Year 3+ |
| **Damara/Nama** | 130,000 | 5% | Phase 4 | Year 3+ |
| **Lozi** | 130,000 | 5% | Phase 4 | Year 3+ |
| **German** | 26,000 | 1% | Phase 5 | Future |

**Strategic Importance:**
- **Oshiwambo = CRITICAL** (49% of population, northern region untapped without translation)
- **Northern Campuses:** UNAM Oshakati, Ongwediva, Ogongo = Oshiwambo-speaking
- **Market Expansion:** Cannot reach northern Namibia schools/clubs without Oshiwambo

### 12.2 Implementation (i18next)

**Installation:**
```bash
npm install i18next react-i18next i18next-browser-languagedetector i18next-http-backend
```

**Configuration:**
```typescript
// src/i18n/config.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpBackend from 'i18next-http-backend';

i18n
  .use(HttpBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    supportedLngs: ['en', 'af', 'osh'], // English, Afrikaans, Oshiwambo
    debug: process.env.NODE_ENV === 'development',
    
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
    
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    
    interpolation: {
      escapeValue: false, // React already escapes
    },
    
    react: {
      useSuspense: false, // Important for SSR
    },
  });

export default i18n;
```

**Translation Files:**
```
/public/locales/
├── en/
│   ├── common.json
│   ├── matches.json
│   ├── players.json
│   └── errors.json
├── af/
│   ├── common.json
│   ├── matches.json
│   ├── players.json
│   └── errors.json
└── osh/ (Phase 2)
    ├── common.json
    ├── matches.json
    ├── players.json
    └── errors.json
```

**Example Translations:**

```json
// /public/locales/en/common.json
{
  "nav": {
    "dashboard": "Dashboard",
    "matches": "Matches",
    "players": "Players",
    "teams": "Teams",
    "analytics": "Analytics"
  },
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "upload": "Upload",
    "download": "Download"
  },
  "match": {
    "status": {
      "live": "Live",
      "completed": "Completed",
      "scheduled": "Scheduled"
    },
    "upload_success": "Match uploaded successfully",
    "analysis_ready": "Your match analysis is ready to view"
  }
}

// /public/locales/af/common.json
{
  "nav": {
    "dashboard": "Dashboard",
    "matches": "Wedstryde",
    "players": "Spelers",
    "teams": "Spanne",
    "analytics": "Analise"
  },
  "actions": {
    "save": "Stoor",
    "cancel": "Kanselleer",
    "delete": "Verwyder",
    "upload": "Oplaai",
    "download": "Aflaai"
  },
  "match": {
    "status": {
      "live": "Lewendig",
      "completed": "Voltooi",
      "scheduled": "Geskeduleer"
    },
    "upload_success": "Wedstryd suksesvol opgelaai",
    "analysis_ready": "Jou wedstryd analise is gereed"
  }
}

// /public/locales/osh/common.json (Phase 2 - Native speaker translation required)
{
  "nav": {
    "dashboard": "Dashboard",
    "matches": "Omayendelo",
    "players": "Oovaluki",
    "teams": "Oikweta",
    "analytics": "Ombito"
  },
  "actions": {
    "save": "Konga",
    "cancel": "Tandula",
    "delete": "Hwitula",
    "upload": "Tumika",
    "download": "Eta"
  },
  "match": {
    "status": {
      "live": "Oku li heni",
      "completed": "Ye li pwa",
      "scheduled": "Ye li longitha"
    },
    "upload_success": "Omuyendelo gwe li tumikwa ka",
    "analysis_ready": "Ombito yomuyendelo go ye li pita"
  }
}
```

**Component Usage:**
```typescript
// src/components/MatchCard.tsx
import { useTranslation } from 'react-i18next';

export const MatchCard = ({ match }) => {
  const { t } = useTranslation('common');
  
  return (
    <div className="match-card">
      <h3>{t('nav.matches')}</h3>
      <span className="status">
        {t(`match.status.${match.status}`)}
      </span>
      <button>{t('actions.download')}</button>
    </div>
  );
};
```

**Language Switcher:**
```typescript
// src/components/LanguageSwitcher.tsx
import { useTranslation } from 'react-i18next';

export const LanguageSwitcher = () => {
  const { i18n } = useTranslation();
  
  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'af', name: 'Afrikaans', flag: '🇿🇦' },
    { code: 'osh', name: 'Oshiwambo', flag: '🇳🇦', comingSoon: true },
  ];
  
  return (
    <select
      value={i18n.language}
      onChange={(e) => i18n.changeLanguage(e.target.value)}
      className="language-switcher"
    >
      {languages.map((lang) => (
        <option key={lang.code} value={lang.code} disabled={lang.comingSoon}>
          {lang.flag} {lang.name} {lang.comingSoon && '(Coming Soon)'}
        </option>
      ))}
    </select>
  );
};
```

### 12.3 Cultural Localization

**Date & Time Formats (Namibia):**
```typescript
// src/utils/formatters.ts
import { format } from 'date-fns';
import { enUS, af } from 'date-fns/locale';

export const formatDate = (date: Date, language: string) => {
  const locales = { en: enUS, af: af };
  
  return format(date, 'dd/MM/yyyy', { 
    locale: locales[language] || enUS 
  });
};

// Namibia uses:
// - Date: DD/MM/YYYY (European style)
// - Time: 24-hour format (14:00 not 2:00 PM)
// - Timezone: CAT (Central Africa Time, UTC+2)
```

**Number & Currency Formatting:**
```typescript
export const formatCurrency = (amount: number, language: string) => {
  return new Intl.NumberFormat(language === 'en' ? 'en-NA' : 'af-NA', {
    style: 'currency',
    currency: 'NAD',
    currencyDisplay: 'symbol',
  }).format(amount);
};

// Output: N$ 1,234.56 (space after symbol, comma thousands, period decimal)
```

**Sports-Specific Terminology:**
```json
// Localized sport names
{
  "sports": {
    "football": {
      "en": "Football",
      "af": "Sokker",
      "osh": "Omupira"
    },
    "basketball": {
      "en": "Basketball",
      "af": "Basketbal",
      "osh": "Omupira wosipeki"
    },
    "rugby": {
      "en": "Rugby",
      "af": "Rugby",
      "osh": "Rugby"
    }
  }
}
```

### 12.4 Translation Quality Control

**Process:**
1. **Professional Translation:** Hire native Namibian translators (not Google Translate)
2. **Community Review:** UNAM students, coaches beta test translations
3. **In-App Feedback:** "Report Translation Error" button (context-specific)
4. **Quarterly Updates:** Review feedback, improve translations
5. **Style Guide:** Formal vs informal (sports = casual in Namibia)

**Oshiwambo Translation (Phase 2):**
- **Budget:** N$50,000 (8-week project)
- **Translator:** Native speaker from Oshakati/Ongwediva region
- **Dialects:** Focus on Oshindonga (most widely understood)
- **Review:** UNAM students + northern campus coordinators
- **Testing:** 50 northern Namibia users (beta program)

**Translation Costs:**
| Language | UI Strings | Cost | Timeline |
|----------|-----------|------|----------|
| English | 1,000+ | Baseline | ✅ Complete |
| Afrikaans | 1,000+ | N$30,000 | ✅ Complete |
| Oshiwambo | 1,000+ | N$50,000 | Month 6-9 |
| Otjiherero | 1,000+ | N$40,000 | Year 2 |
| Others | 1,000+ each | N$40,000 each | Year 3+ |

### 12.5 RTL & Bidirectional Support

**Not Required:** All Namibian languages use Latin script (left-to-right)
- No need for RTL (Right-to-Left) support
- No need for bidirectional text
- Simplifies implementation vs Arabic/Hebrew support

### 12.6 SMS & WhatsApp Localization

**Language-Specific Notifications:**
```typescript
// English
"Your match analysis for UNAM FC vs African Stars is ready. View: [link]"

// Afrikaans
"Jou wedstryd analise vir UNAM FC vs African Stars is gereed. Kyk: [link]"

// Oshiwambo (Phase 2 - Requires native validation)
"Ombito yomuyendelo gUNAM FC nAfrican Stars ye li pita. Kala: [link]"
```

**Character Limits:**
- SMS: 160 characters (Latin alphabet)
- WhatsApp: 4,096 characters (no practical limit)
- Recommendation: Keep SMS <140 chars (allow for encoding overhead)

---

## 13. Multi-Sport Architecture

### 13.1 Sport Configuration System

**Core Philosophy:** Configuration over hardcoding - all sport-specific behavior driven by `SportConfig` objects.

```typescript
// types/sport.ts
export interface SportConfig {
  id: string;                    // 'football', 'basketball', 'rugby', etc.
  name: string;                 // Display name
  icon: string;                 // Sport icon/emoji
  
  // Playing area
  field: {
    type: 'rectangular' | 'court' | 'pitch' | 'track';
    dimensions: { width: number; height: number; unit: string };
    zones?: Zone[];              // Defined areas (penalty box, 3-point line, etc.)
    visualizationType: 'field' | 'court' | 'track' | 'custom';
  };
  
  // Scoring system
  scoring: {
    pointTypes: ScoreType[];     // goal, basket, try, run, ace
    maxScore?: number;           // For set-based sports
    overtimeRules?: OvertimeRule;
  };
  
  // Time structure
  time: {
    periods: number;             // Halves, quarters, sets, innings
    periodDuration?: number;     // Minutes per period (null for cricket, tennis)
    periodNames: string[];       // ['1st Half', '2nd Half'] or ['Set 1', 'Set 2']
    hasTimer: boolean;           // True for timed sports, false for cricket/tennis
  };
  
  // Player positions
  positions: {
    categories: PositionCategory[];  // Offense, Defense, Specialized
    maxPlayers: number;              // On field/court at once
    substitutionRules: SubRule;
  };
  
  // Event types
  events: {
    scoreEvents: string[];       // 'goal', 'basket', 'try', 'run'
    penaltyEvents: string[];     // 'yellow_card', 'foul', 'sin_bin'
    gameEvents: string[];        // 'substitution', 'timeout', 'injury'
  };
  
  // Metrics
  metrics: {
    primary: Metric[];           // Distance, points, rebounds, tackles
    secondary: Metric[];         // Advanced stats
    units: { [key: string]: string };  // km, mph, etc.
  };
}
```

**Example Configuration:**
```typescript
// config/sports/football.config.ts
export const FOOTBALL_CONFIG: SportConfig = {
  id: 'football',
  name: 'Football',
  icon: '⚽',
  field: {
    type: 'rectangular',
    dimensions: { width: 105, height: 68, unit: 'meters' },
    zones: [
      { id: 'penalty_box', name: 'Penalty Box', coordinates: [...] },
      { id: 'goal_area', name: 'Goal Area', coordinates: [...] },
    ],
    visualizationType: 'field',
  },
  scoring: {
    pointTypes: [{ type: 'goal', value: 1 }],
  },
  time: {
    periods: 2,
    periodDuration: 45,
    periodNames: ['1st Half', '2nd Half'],
    hasTimer: true,
  },
  positions: {
    categories: [
      { id: 'goalkeeper', name: 'Goalkeeper', maxPlayers: 1 },
      { id: 'defender', name: 'Defender', maxPlayers: 4 },
      { id: 'midfielder', name: 'Midfielder', maxPlayers: 4 },
      { id: 'forward', name: 'Forward', maxPlayers: 2 },
    ],
    maxPlayers: 11,
    substitutionRules: { maxSubs: 5, rolling: true },
  },
  events: {
    scoreEvents: ['goal'],
    penaltyEvents: ['yellow_card', 'red_card', 'foul'],
    gameEvents: ['substitution', 'injury', 'offside'],
  },
  metrics: {
    primary: [
      { id: 'distance', name: 'Distance Covered', unit: 'km' },
      { id: 'sprints', name: 'Sprints', unit: 'count' },
      { id: 'passes', name: 'Passes', unit: 'count' },
    ],
    secondary: [
      { id: 'heatmap', name: 'Heatmap', unit: 'density' },
      { id: 'pass_accuracy', name: 'Pass Accuracy', unit: '%' },
    ],
    units: { distance: 'km', speed: 'km/h', passes: 'count' },
  },
};
```

### 13.2 Sport Adapter Pattern

**Purpose:** Transform sport-specific data into universal format for generic components.

```typescript
// types/adapter.ts
export interface ISportAdapter {
  sport: SportConfig;
  
  // Data transformation
  transformMatch(match: any): UniversalMatch;
  transformPlayer(player: any): UniversalPlayer;
  transformEvent(event: any): UniversalEvent;
  
  // Formatting
  formatScore(score: any): string;
  formatTime(time: number): string;
  formatMetric(metric: string, value: number): string;
  
  // Rendering helpers
  getEventIcon(eventType: string): string;
  getPositionName(positionId: string): string;
  getZoneColor(zoneId: string): string;
}

// adapters/FootballAdapter.ts
export class FootballAdapter implements ISportAdapter {
  sport = FOOTBALL_CONFIG;
  
  transformMatch(match: any): UniversalMatch {
    return {
      id: match.id,
      teams: [
        { id: match.home_team.id, name: match.home_team.name, score: match.home_score },
        { id: match.away_team.id, name: match.away_team.name, score: match.away_score },
      ],
      status: match.status,
      period: match.current_period || '1st Half',
      time: match.match_time || 0,
    };
  }
  
  formatScore(score: any): string {
    return `${score.home} - ${score.away}`;
  }
  
  formatTime(time: number): string {
    const minutes = Math.floor(time / 60);
    return `${minutes}'`;
  }
  
  getEventIcon(eventType: string): string {
    const icons = {
      goal: '⚽',
      yellow_card: '🟨',
      red_card: '🟥',
      substitution: '🔄',
    };
    return icons[eventType] || '•';
  }
}

// adapters/SportAdapterFactory.ts
export class SportAdapterFactory {
  private adapters: Map<string, ISportAdapter> = new Map();
  
  constructor() {
    this.register('football', new FootballAdapter());
    this.register('basketball', new BasketballAdapter());
    this.register('rugby', new RugbyAdapter());
    // ... register all 8 sports
  }
  
  register(sportId: string, adapter: ISportAdapter): void {
    this.adapters.set(sportId, adapter);
  }
  
  getAdapter(sportId: string): ISportAdapter {
    const adapter = this.adapters.get(sportId);
    if (!adapter) {
      throw new Error(`No adapter found for sport: ${sportId}`);
    }
    return adapter;
  }
}

export const sportAdapterFactory = new SportAdapterFactory();
```

### 13.3 Universal Component Architecture

**13 Universal Components** that work across all sports:

```typescript
// components/universal/MatchCard.tsx
interface MatchCardProps {
  match: UniversalMatch;
  sport: SportConfig;
  adapter: ISportAdapter;
}

export const MatchCard = ({ match, sport, adapter }: MatchCardProps) => {
  const formattedScore = adapter.formatScore(match.score);
  const formattedTime = adapter.formatTime(match.time);
  
  return (
    <div className="match-card">
      <div className="match-header">
        <span className="sport-icon">{sport.icon}</span>
        <span className="sport-name">{sport.name}</span>
      </div>
      <div className="teams">
        <TeamDisplay team={match.teams[0]} />
        <div className="score">{formattedScore}</div>
        <TeamDisplay team={match.teams[1]} />
      </div>
      <div className="match-info">
        <span>{match.period}</span>
        <span>{formattedTime}</span>
      </div>
    </div>
  );
};

// components/universal/PlayingAreaVisualization.tsx
interface PlayingAreaVisualizationProps {
  sport: SportConfig;
  events: UniversalEvent[];
  heatmap?: HeatmapData;
}

export const PlayingAreaVisualization = ({ 
  sport, 
  events, 
  heatmap 
}: PlayingAreaVisualizationProps) => {
  const FieldRenderer = getFieldRenderer(sport.field.type);
  
  return (
    <div className="playing-area">
      <FieldRenderer
        dimensions={sport.field.dimensions}
        zones={sport.field.zones}
        events={events}
        heatmap={heatmap}
      />
    </div>
  );
};

// components/universal/StatCard.tsx
interface StatCardProps {
  metric: Metric;
  value: number;
  sport: SportConfig;
  adapter: ISportAdapter;
}

export const StatCard = ({ metric, value, sport, adapter }: StatCardProps) => {
  const formatted = adapter.formatMetric(metric.id, value);
  const unit = sport.metrics.units[metric.id] || '';
  
  return (
    <div className="stat-card">
      <div className="stat-label">{metric.name}</div>
      <div className="stat-value">{formatted}</div>
      {unit && <div className="stat-unit">{unit}</div>}
    </div>
  );
};
```

### 13.4 Sport Context Provider

```typescript
// contexts/SportContext.tsx
import { createContext, useContext, useState } from 'react';
import { SportConfig } from '@/types/sport';
import { ISportAdapter } from '@/types/adapter';
import { sportAdapterFactory } from '@/adapters/SportAdapterFactory';

interface SportContextType {
  currentSport: SportConfig;
  adapter: ISportAdapter;
  setSport: (sportId: string) => void;
  availableSports: SportConfig[];
}

const SportContext = createContext<SportContextType | null>(null);

export const SportProvider = ({ children }: { children: React.ReactNode }) => {
  const [sportId, setSportId] = useState<string>('football');
  const adapter = sportAdapterFactory.getAdapter(sportId);
  
  const setSport = (newSportId: string) => {
    setSportId(newSportId);
  };
  
  return (
    <SportContext.Provider
      value={{
        currentSport: adapter.sport,
        adapter,
        setSport,
        availableSports: ALL_SPORTS,
      }}
    >
      {children}
    </SportContext.Provider>
  );
};

export const useSport = () => {
  const context = useContext(SportContext);
  if (!context) {
    throw new Error('useSport must be used within SportProvider');
  }
  return context;
};

// Usage in components
export const MatchDetailPage = () => {
  const { currentSport, adapter } = useSport();
  const { match } = useMatch();
  
  const universalMatch = adapter.transformMatch(match);
  
  return (
    <div>
      <MatchCard match={universalMatch} sport={currentSport} adapter={adapter} />
      <PlayingAreaVisualization sport={currentSport} events={match.events} />
    </div>
  );
};
```

### 13.5 Adding a New Sport (1-Hour Process)

```typescript
// Step 1: Create Sport Configuration (5 min)
// config/sports/newsport.config.ts
export const NEW_SPORT_CONFIG: SportConfig = {
  id: 'newsport',
  name: 'New Sport',
  icon: '🏀',
  field: { /* ... */ },
  scoring: { /* ... */ },
  time: { /* ... */ },
  positions: { /* ... */ },
  events: { /* ... */ },
  metrics: { /* ... */ },
};

// Step 2: Create Adapter (15 min)
// adapters/NewSportAdapter.ts
export class NewSportAdapter implements ISportAdapter {
  sport = NEW_SPORT_CONFIG;
  
  transformMatch(match: any): UniversalMatch {
    // Transform sport-specific data to universal format
  }
  
  formatScore(score: any): string {
    // Format score display
  }
  
  // ... implement all interface methods
}

// Step 3: Register Adapter (5 min)
// adapters/SportAdapterFactory.ts
constructor() {
  // ... existing registrations
  this.register('newsport', new NewSportAdapter());
}

// Step 4: Add Assets (10 min)
// public/icons/sports/newsport.svg
// public/images/fields/newsport-field.png

// Step 5: Test (30 min)
// All 13 universal components work automatically!
```

**Result:** Zero code changes to existing components - new sport works immediately.

---

## 14. Offline-First Implementation

### 14.1 Service Worker Setup (Workbox)

```typescript
// public/sw.js (Service Worker)
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Precache static assets
precacheAndRoute(self.__WB_MANIFEST);

// Cache API responses (NetworkFirst for freshness)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 24 * 60 * 60, // 24 hours
      }),
    ],
  })
);

// Cache images (CacheFirst for performance)
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
      }),
    ],
  })
);

// Background sync for offline actions
import { BackgroundSyncPlugin } from 'workbox-background-sync';

const bgSyncPlugin = new BackgroundSyncPlugin('match-upload-queue', {
  maxRetentionTime: 24 * 60, // 24 hours
});

registerRoute(
  ({ url }) => url.pathname === '/api/matches/upload',
  new NetworkFirst({
    plugins: [bgSyncPlugin],
  }),
  'POST'
);
```

### 14.2 IndexedDB for Offline Storage

```typescript
// lib/db.ts (Dexie.js wrapper)
import Dexie, { Table } from 'dexie';

interface Match {
  id: string;
  data: any;
  synced: boolean;
  lastModified: number;
}

interface Player {
  id: string;
  data: any;
  synced: boolean;
}

class SportsAnalyticsDB extends Dexie {
  matches!: Table<Match>;
  players!: Table<Player>;
  teams!: Table<any>;
  events!: Table<any>;
  
  constructor() {
    super('SportsAnalyticsDB');
    this.version(1).stores({
      matches: 'id, synced, lastModified',
      players: 'id, synced',
      teams: 'id, synced',
      events: 'id, matchId, timestamp',
    });
  }
}

export const db = new SportsAnalyticsDB();

// Usage: Save match for offline access
export const saveMatchOffline = async (match: any) => {
  await db.matches.put({
    id: match.id,
    data: match,
    synced: false,
    lastModified: Date.now(),
  });
};

// Usage: Sync when online
export const syncOfflineData = async () => {
  const unsyncedMatches = await db.matches.where('synced').equals(false).toArray();
  
  for (const match of unsyncedMatches) {
    try {
      await api.matches.upload(match.data);
      await db.matches.update(match.id, { synced: true });
    } catch (error) {
      console.error('Sync failed:', error);
    }
  }
};
```

### 14.3 Offline-First Data Fetching

```typescript
// hooks/useOfflineMatch.ts
import { useQuery } from '@tanstack/react-query';
import { db } from '@/lib/db';

export const useOfflineMatch = (matchId: string) => {
  return useQuery(
    ['match', matchId],
    async () => {
      // Try network first
      try {
        const match = await api.matches.getById(matchId);
        // Cache for offline
        await db.matches.put({
          id: matchId,
          data: match,
          synced: true,
          lastModified: Date.now(),
        });
        return match;
      } catch (error) {
        // Fallback to offline cache
        const cached = await db.matches.get(matchId);
        if (cached) {
          return cached.data;
        }
        throw error;
      }
    },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 24 * 60 * 60 * 1000, // 24 hours
      retry: false, // Don't retry if offline
    }
  );
};
```

### 14.4 Network Status Detection

```typescript
// hooks/useNetworkStatus.ts
import { useEffect, useState } from 'react';
import NetInfo from '@react-native-community/netinfo';

export const useNetworkStatus = () => {
  const [isOnline, setIsOnline] = useState(true);
  const [connectionType, setConnectionType] = useState<string>('unknown');
  
  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? false);
      setConnectionType(state.type);
    });
    
    return () => unsubscribe();
  }, []);
  
  return { isOnline, connectionType, isSlowConnection: connectionType === 'cellular' };
};

// Usage: Show offline indicator
export const OfflineIndicator = () => {
  const { isOnline } = useNetworkStatus();
  
  if (isOnline) return null;
  
  return (
    <div className="offline-banner">
      <span>📡 Offline Mode - Data will sync when connection is restored</span>
    </div>
  );
};
```

---

## 15. Network Optimization for 3G (Namibian Market)

### 15.1 Data Compression

```typescript
// utils/compression.ts
import pako from 'pako';

export const compressData = (data: any): string => {
  const json = JSON.stringify(data);
  const compressed = pako.deflate(json, { to: 'string' });
  return btoa(compressed); // Base64 encode
};

export const decompressData = (compressed: string): any => {
  const binary = atob(compressed);
  const decompressed = pako.inflate(binary, { to: 'string' });
  return JSON.parse(decompressed);
};

// API client with compression
apiClient.interceptors.request.use((config) => {
  if (config.data && config.data.size > 1000) {
    config.data = compressData(config.data);
    config.headers['Content-Encoding'] = 'gzip';
  }
  return config;
});
```

### 15.2 Image Optimization

```typescript
// components/OptimizedImage.tsx
import Image from 'next/image';
import { useState } from 'react';

export const OptimizedImage = ({ src, alt, ...props }) => {
  const [isLoading, setIsLoading] = useState(true);
  const { connectionType } = useNetworkStatus();
  
  // Use lower quality on 3G
  const quality = connectionType === 'cellular' ? 60 : 85;
  
  return (
    <Image
      src={src}
      alt={alt}
      quality={quality}
      loading="lazy"
      placeholder="blur"
      onLoad={() => setIsLoading(false)}
      {...props}
    />
  );
};

// Client-side image compression before upload
import Compressor from 'compressorjs';

export const compressImage = (file: File): Promise<File> => {
  return new Promise((resolve, reject) => {
    new Compressor(file, {
      quality: 0.6, // 60% quality for 3G
      maxWidth: 1920,
      maxHeight: 1080,
      convertTypes: ['image/png'],
      convertSize: 5000000, // Convert PNG > 5MB to JPEG
      success: (compressed) => resolve(compressed as File),
      error: reject,
    });
  });
};
```

### 15.3 Lazy Loading & Code Splitting

```typescript
// Lazy load heavy components
const Heatmap = lazy(() => import('@/components/analytics/Heatmap'));
const PassNetwork = lazy(() => import('@/components/analytics/PassNetwork'));
const VideoPlayer = lazy(() => import('@/components/analytics/VideoPlayer'));

// Intersection Observer for lazy loading
import { useInView } from 'react-intersection-observer';

export const LazyHeatmap = ({ data }) => {
  const { ref, inView } = useInView({
    triggerOnce: true,
    rootMargin: '200px', // Load 200px before visible
  });
  
  return (
    <div ref={ref}>
      {inView ? (
        <Suspense fallback={<HeatmapSkeleton />}>
          <Heatmap data={data} />
        </Suspense>
      ) : (
        <HeatmapSkeleton />
      )}
    </div>
  );
};
```

### 15.4 Request Batching & Debouncing

```typescript
// utils/requestBatcher.ts
class RequestBatcher {
  private queue: Array<{ url: string; resolve: Function; reject: Function }> = [];
  private timer: NodeJS.Timeout | null = null;
  
  batch(url: string): Promise<any> {
    return new Promise((resolve, reject) => {
      this.queue.push({ url, resolve, reject });
      
      if (this.timer) clearTimeout(this.timer);
      
      this.timer = setTimeout(() => {
        this.flush();
      }, 100); // Batch requests within 100ms
    });
  }
  
  private async flush() {
    const urls = this.queue.map(item => item.url);
    const results = await Promise.all(urls.map(url => api.get(url)));
    
    this.queue.forEach((item, index) => {
      item.resolve(results[index]);
    });
    
    this.queue = [];
  }
}

export const requestBatcher = new RequestBatcher();
```

### 15.5 Progressive Data Loading

```typescript
// Load critical data first, then enhance
export const useProgressiveMatch = (matchId: string) => {
  // Critical: Match basics
  const { data: match } = useQuery(['match', matchId], () => 
    api.matches.getById(matchId, { fields: 'basic' })
  );
  
  // Secondary: Analytics (load after match loaded)
  const { data: analytics } = useQuery(
    ['match', matchId, 'analytics'],
    () => api.matches.getAnalytics(matchId),
    { enabled: !!match }
  );
  
  // Tertiary: Video (load last)
  const { data: video } = useQuery(
    ['match', matchId, 'video'],
    () => api.matches.getVideo(matchId),
    { enabled: !!analytics }
  );
  
  return { match, analytics, video };
};
```

---

## 16. Performance Monitoring

### 16.1 Metrics Collection

```typescript
// Performance monitoring setup
import { onCLS, onFID, onLCP } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  // Send to your analytics service
  console.log(metric);
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
```

### 16.2 Error Tracking

```typescript
// Error boundary and tracking
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

## 17. Development Workflow

### 17.1 Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### 17.2 Code Quality

- **Linting:** ESLint with Next.js config
- **Formatting:** Prettier
- **Type Checking:** TypeScript strict mode
- **Pre-commit Hooks:** Husky + lint-staged

## 18. Deployment & Production

### 18.1 Deployment Checklist

- [ ] Environment variables configured
- [ ] API endpoints updated for production
- [ ] Build optimization enabled
- [ ] Error tracking configured
- [ ] Analytics integrated
- [ ] Performance monitoring active
- [ ] Security headers configured
- [ ] CDN configured (if applicable)
- [ ] PWA manifest configured
- [ ] Service worker registered
- [ ] Offline functionality tested
- [ ] Multi-sport configurations verified
- [ ] Localization files deployed
- [ ] Network optimization tested on 3G

### 18.2 Production Build Configuration

```javascript
// next.config.js (Production)
module.exports = {
  output: 'standalone',
  compress: true,
  poweredByHeader: false,
  generateEtags: true,
  images: {
    domains: ['api.sportsanalytics.na'],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  experimental: {
    optimizeCss: true,
  },
  // PWA configuration
  pwa: {
    dest: 'public',
    register: true,
    skipWaiting: true,
    disable: process.env.NODE_ENV === 'development',
  },
};
```

### 18.3 Environment-Specific Configuration

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.sportsanalytics.na/api/v1
NEXT_PUBLIC_WS_URL=wss://api.sportsanalytics.na
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_SENTRY_DSN=...
NEXT_PUBLIC_ANALYTICS_ID=...
```

---

## 19. Security Considerations

### 19.1 Authentication & Authorization

```typescript
// lib/auth.ts
import { getSession } from 'next-auth/react';

export const requireAuth = async (context: GetServerSidePropsContext) => {
  const session = await getSession(context);
  
  if (!session) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }
  
  return { props: { session } };
};

// API route protection
export const withAuth = (handler: NextApiHandler) => {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token || !verifyToken(token)) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    return handler(req, res);
  };
};
```

### 19.2 Content Security Policy

```javascript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
      connect-src 'self' https://api.sportsanalytics.na wss://api.sportsanalytics.na;
    `.replace(/\s{2,}/g, ' ').trim()
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### 19.3 Data Validation

```typescript
// lib/validation.ts
import { z } from 'zod';

export const matchUploadSchema = z.object({
  file: z.instanceof(File).refine(
    (file) => file.size <= 500 * 1024 * 1024, // 500MB max
    'File size must be less than 500MB'
  ),
  team1: z.string().min(1),
  team2: z.string().min(1),
  competition: z.string().min(1),
  date: z.string().datetime(),
});

export const validateMatchUpload = (data: unknown) => {
  return matchUploadSchema.parse(data);
};
```

---

## 20. Troubleshooting & Common Issues

### 20.1 Offline Functionality Issues

**Problem:** Service worker not registering
```typescript
// Check service worker registration
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(reg => console.log('SW registered:', reg))
    .catch(err => console.error('SW registration failed:', err));
}
```

**Problem:** IndexedDB not persisting data
```typescript
// Check IndexedDB support
if (!window.indexedDB) {
  console.error('IndexedDB not supported');
  // Fallback to localStorage
}
```

### 20.2 Network Optimization Issues

**Problem:** Large bundle size on 3G
- Solution: Enable code splitting, lazy load heavy components
- Check: `npm run build` and review bundle analyzer

**Problem:** Images loading slowly
- Solution: Use Next.js Image component with quality reduction
- Check: Network tab for image sizes

### 20.3 Multi-Sport Issues

**Problem:** Sport adapter not found
```typescript
// Check adapter registration
const adapter = sportAdapterFactory.getAdapter('football');
if (!adapter) {
  console.error('Adapter not registered');
}
```

**Problem:** Sport config missing fields
- Solution: Validate SportConfig against TypeScript interface
- Check: All required fields present in config

---

## 21. References

### External Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Documentation](https://tanstack.com/query)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [D3.js Documentation](https://d3js.org/)
- [Recharts Documentation](https://recharts.org/)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [Dexie.js Documentation](https://dexie.org/)

### Internal Documentation
- [API Documentation](API_DOCUMENTATION.md) - Backend API reference
- [UI/UX Design Documentation](UI_UX_DESIGN.md) - Complete wireframes and design system
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements
- [Architecture Documentation](architecture.md) - System architecture
- [Web Dashboard Quick Start](WEB_DASHBOARD_QUICKSTART.md) - Setup guide

---

## 22. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial frontend architecture |
| 1.1 | December 2024 | Added component architecture, state management |
| 2.0 | January 2025 | Namibian optimizations (offline-first, PWA, mobile-first) |
| 2.1 | January 2025 | Comprehensive localization strategy (Section 12: Oshiwambo 49%, Afrikaans 11%, i18next implementation, N$50K Phase 2 translation), Namibian-specific libraries (Workbox, MTC Mobile Money SDK, WhatsApp Business API, Africa's Talking SMS), network conditions (3G 60%, mobile 108% penetration) |
| 2.2 | January 2025 | Multi-sport architecture (Section 13: SportConfig system, ISportAdapter pattern, 13 universal components, SportContext provider, 1-hour new sport addition process), Offline-first implementation (Section 14: Workbox service worker, IndexedDB with Dexie.js, offline data sync, network status detection), Network optimization for 3G (Section 15: data compression, image optimization, lazy loading, request batching, progressive data loading), Complete document structure (Sections 16-22: Performance monitoring, development workflow, deployment & production, security, troubleshooting, references, document history) |

**Major Updates in v2.1:**
- ✅ Localization & Internationalization (Section 12) - Complete Oshiwambo translation strategy
- ✅ Namibian language landscape (13 languages, priorities, timelines, costs)
- ✅ Cultural localization (date/time/currency formats, sports terminology)
- ✅ Translation quality control process (native speakers, community review)
- ✅ SMS/WhatsApp notification templates (3 languages)
- ✅ Namibian-specific tech stack (MTC Mobile Money, PWA, offline sync)

**Major Updates in v2.2:**
- ✅ Multi-Sport Architecture (Section 13) - Complete SportConfig system, ISportAdapter pattern, 13 universal components
- ✅ Sport Context Provider - Global sport state management
- ✅ 1-Hour New Sport Addition Process - Zero code changes to existing components
- ✅ Offline-First Implementation (Section 14) - Workbox service worker, IndexedDB storage, background sync
- ✅ Network Optimization for 3G (Section 15) - Data compression, image optimization, lazy loading, request batching
- ✅ Progressive Data Loading - Critical data first, then enhance
- ✅ Performance Monitoring (Section 16) - Web vitals, error tracking with Sentry
- ✅ Development Workflow (Section 17) - Local development, code quality tools
- ✅ Deployment & Production (Section 18) - Production build config, deployment checklist, environment setup
- ✅ Security Considerations (Section 19) - Authentication, CSP headers, data validation
- ✅ Troubleshooting Guide (Section 20) - Common issues and solutions
- ✅ Complete References (Section 21) - External and internal documentation links

---

**Document Status:** ✅ COMPREHENSIVE - FRONTEND ARCHITECTURE COMPLETE  
**Last Updated:** January 2025  
**Version:** 2.2 (Multi-Sport Architecture + Offline-First + 3G Optimization)  
**Next Review:** Post-launch feedback (Month 3)

---

**For implementation details, see:**
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Regulatory compliance, financial analysis, market research
- [Web Dashboard Quick Start](WEB_DASHBOARD_QUICKSTART.md) - Setup guide
- [UI/UX Design Documentation](UI_UX_DESIGN.md) - Complete wireframes and multi-sport design system
- [Architecture Documentation](architecture.md) - Infrastructure resilience, load shedding mitigation
- [API Documentation](API_DOCUMENTATION.md) - Offline-first sync, network optimization
- [UNAM 13 Campuses Strategy](UNAM_13_CAMPUSES_STRATEGY.md) - Anchor client strategy

