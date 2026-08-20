export interface EmailMessage {
  id: string;
  threadId: string;
  sender: string;
  subject: string;
  snippet: string;
  body: string;
  date: Date;
  labels: string[];
  isUnread: boolean;
}

export interface LinkedInNotification {
  id: string;
  type: string;
  actor: {
    name: string;
    profileUrl?: string;
  };
  action: string;
  timestamp: Date;
  description: string;
  url?: string;
}

export interface DailyReport {
  generatedAt: Date;
  period: {
    startDate: Date;
    endDate: Date;
  };
  sections: {
    emails: ReportSection;
    linkedin: ReportSection;
  };
}

export interface ReportSection {
  title: string;
  count: number;
  items: ReportItem[];
}

export interface ReportItem {
  title: string;
  summary: string;
  source: string;
  timestamp: Date;
  url?: string;
}

export interface AppConfig {
  gmailClientId: string;
  gmailClientSecret: string;
  gmailRedirectUri: string;
  linkedinClientId: string;
  linkedinClientSecret: string;
  linkedinAccessToken: string;
  scheduleTime: string;
  reportOutputDir: string;
  gmailUserEmail: string;
}
