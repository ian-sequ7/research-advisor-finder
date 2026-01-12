'use client';

import Link from 'next/link';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  GraduationCap,
  Mail,
  Coffee,
  HelpCircle,
  Calendar,
  AlertTriangle,
  ChevronLeft,
  CheckCircle,
  XCircle,
  Clock,
  Users,
  BookOpen,
  ExternalLink,
} from 'lucide-react';

export default function Resources() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
      <div className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="h-6 w-6 text-primary" />
            <h1 className="text-xl font-semibold">Resources</h1>
          </div>
          <Link
            href="/"
            className="text-sm text-muted-foreground hover:text-primary flex items-center gap-1"
          >
            <ChevronLeft className="h-4 w-4" />
            Back to Search
          </Link>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {/* Intro */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold mb-2">
            How to Find Your Perfect Research Advisor
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            A comprehensive guide to cold emailing professors, conducting coffee chats,
            and evaluating potential PhD advisors.
          </p>
        </div>

        {/* Table of Contents */}
        <Card>
          <CardHeader className="pb-3">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Quick Navigation
            </h3>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
              <a href="#cold-email" className="text-primary hover:underline flex items-center gap-2">
                <Mail className="h-4 w-4" /> Cold Email Guide
              </a>
              <a href="#coffee-chat" className="text-primary hover:underline flex items-center gap-2">
                <Coffee className="h-4 w-4" /> Coffee Chat Best Practices
              </a>
              <a href="#questions" className="text-primary hover:underline flex items-center gap-2">
                <HelpCircle className="h-4 w-4" /> Questions to Ask Advisors
              </a>
              <a href="#timeline" className="text-primary hover:underline flex items-center gap-2">
                <Calendar className="h-4 w-4" /> PhD Application Timeline
              </a>
              <a href="#red-flags" className="text-primary hover:underline flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" /> Red Flags to Watch For
              </a>
            </div>
          </CardContent>
        </Card>

        {/* Section 1: Cold Email */}
        <Card id="cold-email">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Mail className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">How to Write a Cold Email</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              Your first impression matters. Here&apos;s how to craft an email that gets responses.
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Email Structure */}
            <div>
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                Email Structure (3-4 Short Paragraphs Max)
              </h4>
              <div className="space-y-3 text-sm">
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="font-medium text-primary mb-1">1. Introduction (1-2 sentences)</p>
                  <p className="text-muted-foreground">
                    Your name, current position, and how you found them.
                  </p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="font-medium text-primary mb-1">2. Research Connection (2-3 sentences)</p>
                  <p className="text-muted-foreground">
                    Reference a specific paper they authored. Ask a thoughtful question about their methodology.
                  </p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="font-medium text-primary mb-1">3. Your Background (2-3 sentences)</p>
                  <p className="text-muted-foreground">
                    Briefly mention 1-2 relevant experiences that connect to their work.
                  </p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="font-medium text-primary mb-1">4. The Ask (1-2 sentences)</p>
                  <p className="text-muted-foreground">
                    Request a brief 15-20 minute call to discuss their research.
                  </p>
                </div>
              </div>
            </div>

            <Separator />

            {/* Email Template */}
            <div>
              <h4 className="font-medium mb-3">Email Template</h4>
              <div className="bg-slate-900 text-slate-100 rounded-lg p-4 text-sm font-mono overflow-x-auto">
                <p className="text-yellow-400 mb-2">Subject: Prospective PhD: [Their Research Area] & [Your Skill]</p>
                <div className="space-y-3 text-slate-300">
                  <p>Dear Professor [Last Name],</p>
                  <p>
                    My name is [Your Name], and I am a [Your Position] in [Field] from [University].
                    I am writing to inquire about joining your research group as a PhD student for [Term/Year].
                  </p>
                  <p>
                    I have been following your lab&apos;s work on [Research Area], particularly your recent paper,
                    &quot;[Paper Title],&quot; published in [Venue]. I found your approach to [Specific Detail] innovative.
                    [One thoughtful question about their methodology].
                  </p>
                  <p>
                    My background includes [2 relevant experiences]. I have attached my CV for reference.
                    Would you be available for a brief 20-minute call to discuss potential research directions?
                  </p>
                  <p>
                    Thank you for your time and consideration.<br />
                    Best regards,<br />
                    [Your Name]
                  </p>
                </div>
              </div>
            </div>

            <Separator />

            {/* Do's and Don'ts */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium mb-3 flex items-center gap-2 text-green-700">
                  <CheckCircle className="h-4 w-4" />
                  Do
                </h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">•</span>
                    Reference a specific recent paper
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">•</span>
                    Ask a thoughtful question about their work
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">•</span>
                    Keep it under 200 words
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">•</span>
                    Send during business hours (Tue-Thu optimal)
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">•</span>
                    Proofread for typos and correct title
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-3 flex items-center gap-2 text-red-700">
                  <XCircle className="h-4 w-4" />
                  Don&apos;t
                </h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 mt-1">•</span>
                    Use generic templates with no personalization
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 mt-1">•</span>
                    Write more than 4 paragraphs
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 mt-1">•</span>
                    Get their name or title wrong
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 mt-1">•</span>
                    Send the same email to multiple professors (they talk)
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 mt-1">•</span>
                    Include excessive flattery without substance
                  </li>
                </ul>
              </div>
            </div>

            <Separator />

            {/* Follow-up Timing */}
            <div>
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <Clock className="h-4 w-4" />
                Follow-Up Timing
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                <div className="bg-blue-50 rounded-lg p-3 text-center">
                  <p className="font-medium text-blue-800">First Follow-Up</p>
                  <p className="text-blue-600">7-14 days</p>
                </div>
                <div className="bg-amber-50 rounded-lg p-3 text-center">
                  <p className="font-medium text-amber-800">Weekend Emails</p>
                  <p className="text-amber-600">Wait until Tuesday</p>
                </div>
                <div className="bg-slate-100 rounded-lg p-3 text-center">
                  <p className="font-medium text-slate-800">Max Follow-Ups</p>
                  <p className="text-slate-600">1 (then move on)</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Section 2: Coffee Chat */}
        <Card id="coffee-chat">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Coffee className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Coffee Chat Best Practices</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              How to make the most of your 20-30 minutes with a potential advisor.
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Format */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-slate-50 rounded-lg p-4 text-center">
                <Clock className="h-6 w-6 mx-auto mb-2 text-primary" />
                <p className="font-medium">Duration</p>
                <p className="text-sm text-muted-foreground">15-30 minutes</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-4 text-center">
                <HelpCircle className="h-6 w-6 mx-auto mb-2 text-primary" />
                <p className="font-medium">Structure</p>
                <p className="text-sm text-muted-foreground">20 min questions, 10 min you</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-4 text-center">
                <Users className="h-6 w-6 mx-auto mb-2 text-primary" />
                <p className="font-medium">Format</p>
                <p className="text-sm text-muted-foreground">Video call preferred</p>
              </div>
            </div>

            <Separator />

            {/* Preparation Checklist */}
            <div>
              <h4 className="font-medium mb-3">Preparation Checklist</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                {[
                  'Research their recent publications (last 2-3 years)',
                  'Prepare 5-7 questions (see next section)',
                  'Review current lab members\' profiles',
                  'Prepare 2-minute summary of your background',
                  'Have 1-2 intelligent questions about their recent work',
                  'Test your video/audio setup beforehand',
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 shrink-0" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            {/* Etiquette Tips */}
            <div>
              <h4 className="font-medium mb-3">Etiquette Tips</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <Badge className="bg-blue-100 text-blue-800 shrink-0">Time</Badge>
                  <span>If you requested 30 minutes, wrap up at 30 minutes. Give them an out: &quot;I know we only have a few more minutes...&quot;</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge className="bg-green-100 text-green-800 shrink-0">Follow-Up</Badge>
                  <span>Send a thank-you email within 24 hours referencing something specific from your conversation.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge className="bg-purple-100 text-purple-800 shrink-0">Virtual</Badge>
                  <span>Get their phone number as backup for technical issues. Video is preferred over audio-only.</span>
                </li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Section 3: Questions to Ask */}
        <Card id="questions">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <HelpCircle className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Questions to Ask Potential Advisors</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              These questions will help you evaluate fit and avoid problematic advisors.
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Mentorship Style */}
            <div>
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <Badge className="bg-blue-100 text-blue-800">Critical</Badge>
                Mentorship Style
              </h4>
              <ul className="space-y-2 text-sm">
                <li>• &quot;Do you consider yourself more of a hands-on or hands-off advisor?&quot;</li>
                <li>• &quot;How frequently do you meet with students one-on-one?&quot;</li>
                <li>• &quot;How do you give feedback on papers and research?&quot;</li>
                <li>• &quot;What support do you provide when students struggle?&quot;</li>
              </ul>
            </div>

            <Separator />

            {/* Lab Culture */}
            <div>
              <h4 className="font-medium mb-3">Lab Culture & Structure</h4>
              <ul className="space-y-2 text-sm">
                <li>• &quot;What is the lab structure? How collaborative are projects?&quot;</li>
                <li>• &quot;Are there regular lab meetings? What do they look like?&quot;</li>
                <li>• &quot;Do students work in a shared physical space?&quot;</li>
                <li>• &quot;How would you describe the lab culture?&quot;</li>
              </ul>
            </div>

            <Separator />

            {/* Funding */}
            <div>
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <Badge className="bg-green-100 text-green-800">Important</Badge>
                Funding & Support
              </h4>
              <ul className="space-y-2 text-sm">
                <li>• &quot;Are you accepting students this year, and is the position funded?&quot;</li>
                <li>• &quot;Will funding remain stable throughout my PhD?&quot;</li>
                <li>• &quot;What happens if primary funding ends?&quot;</li>
                <li>• &quot;How do you view students applying for external fellowships?&quot;</li>
              </ul>
            </div>

            <Separator />

            {/* Outcomes */}
            <div>
              <h4 className="font-medium mb-3">Graduation & Career Outcomes</h4>
              <ul className="space-y-2 text-sm">
                <li>• &quot;What is the average time to graduation for your students?&quot;</li>
                <li>• &quot;What have previous students done after graduating?&quot;</li>
                <li>• &quot;How often do you send students to conferences?&quot;</li>
                <li>• &quot;What&apos;s your approach to summer internships?&quot;</li>
              </ul>
            </div>

            <Separator />

            {/* Ask Current Students */}
            <div className="bg-amber-50 rounded-lg p-4">
              <h4 className="font-medium mb-2 flex items-center gap-2 text-amber-800">
                <AlertTriangle className="h-4 w-4" />
                Must Ask Current Students (Privately)
              </h4>
              <ul className="space-y-2 text-sm text-amber-900">
                <li>• &quot;How does the advisor handle conflicts or disagreements?&quot;</li>
                <li>• &quot;Has anyone left the lab? Why?&quot;</li>
                <li>• &quot;What&apos;s the advisor&apos;s actual availability vs. stated availability?&quot;</li>
                <li>• &quot;Do they support career goals even if different from theirs?&quot;</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Section 4: Timeline */}
        <Card id="timeline">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">PhD Application Timeline</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              Month-by-month guide for US PhD programs (Fall admission).
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  months: 'June - July',
                  tasks: 'Research programs and fields. Review NSF GRFP requirements if eligible.',
                  color: 'bg-slate-100',
                },
                {
                  months: 'August - September',
                  tasks: 'Check GRE requirements. Contact letter writers. Draft statements. BEGIN contacting professors.',
                  color: 'bg-blue-50',
                  highlight: true,
                },
                {
                  months: 'October',
                  tasks: 'PRIME TIME for cold emails. Take/retake GRE. Submit NSF GRFP if applicable.',
                  color: 'bg-green-50',
                  highlight: true,
                },
                {
                  months: 'November - December',
                  tasks: 'Finalize statements. Remind letter writers. Submit applications (most deadlines early Dec).',
                  color: 'bg-amber-50',
                },
                {
                  months: 'January',
                  tasks: 'Receive interview invitations. Focus on current commitments.',
                  color: 'bg-slate-100',
                },
                {
                  months: 'February - March',
                  tasks: 'Attend interviews (virtual or in-person). Receive decisions.',
                  color: 'bg-purple-50',
                },
                {
                  months: 'April',
                  tasks: 'Receive fellowship results. COMMIT to program (April 15 deadline).',
                  color: 'bg-green-50',
                  highlight: true,
                },
              ].map((item, i) => (
                <div
                  key={i}
                  className={`rounded-lg p-4 ${item.color} ${item.highlight ? 'border-2 border-primary/30' : ''}`}
                >
                  <div className="flex items-start gap-4">
                    <div className="font-medium text-sm w-36 shrink-0">{item.months}</div>
                    <div className="text-sm">{item.tasks}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 bg-blue-50 rounded-lg p-4">
              <h4 className="font-medium mb-2 text-blue-800">Key Insight</h4>
              <p className="text-sm text-blue-900">
                Contact professors <strong>6+ months before deadlines</strong> (August-October for December deadlines).
                Early contact matters because not all faculty accept students each year, and professors are
                overwhelmed with requests close to deadlines.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Section 5: Red Flags */}
        <Card id="red-flags">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-red-600" />
              <h3 className="text-lg font-semibold">Red Flags in Advisor Relationships</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              Warning signs to watch for when evaluating potential advisors.
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Critical Red Flags */}
            <div>
              <h4 className="font-medium mb-3 flex items-center gap-2 text-red-700">
                <XCircle className="h-4 w-4" />
                Critical Warning Signs
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  {
                    title: 'Poor Communication',
                    desc: 'Emails unanswered for days, mysteriously absent, seeming disinterested',
                  },
                  {
                    title: 'Lack of Mentorship',
                    desc: 'New students receive inadequate training, expecting independence without foundation',
                  },
                  {
                    title: 'Publication Issues',
                    desc: 'Current senior students have no publications, poor publication record',
                  },
                  {
                    title: 'Isolation Tactics',
                    desc: 'Discouraging interaction with other scholars, preventing collaboration',
                  },
                  {
                    title: 'Exploitation',
                    desc: 'Asking to run personal errands, ghostwrite reviews, or unpaid work',
                  },
                  {
                    title: 'Funding Evasiveness',
                    desc: 'Avoiding discussion about funding, unable to guarantee support',
                  },
                ].map((flag, i) => (
                  <div key={i} className="bg-red-50 rounded-lg p-3">
                    <p className="font-medium text-red-800 text-sm">{flag.title}</p>
                    <p className="text-red-700 text-sm">{flag.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            {/* How to Vet */}
            <div>
              <h4 className="font-medium mb-3">How to Vet Advisors</h4>
              <ol className="space-y-2 text-sm list-decimal list-inside">
                <li>Talk to current students <strong>privately</strong> (without advisor present)</li>
                <li>Contact former students who left the lab (find on LinkedIn)</li>
                <li>Check publication records on Google Scholar (Are students first authors?)</li>
                <li>Ask department for average time-to-degree by advisor</li>
                <li>Attend a lab meeting before committing if possible</li>
                <li>Ask about former students who left — how did the advisor respond?</li>
                <li className="font-medium">Trust your gut — if something feels off, it probably is</li>
              </ol>
            </div>

            <Separator />

            {/* If You're Already In a Bad Situation */}
            <div className="bg-amber-50 rounded-lg p-4">
              <h4 className="font-medium mb-2 text-amber-800">If You Realize Your Advisor Is Toxic</h4>
              <p className="text-sm text-amber-900 mb-3">
                The best advice: <strong>Leave as soon as possible.</strong> If you can&apos;t leave immediately:
              </p>
              <ul className="space-y-1 text-sm text-amber-900">
                <li>• Establish other mentors who can write letters of support</li>
                <li>• Start publishing with other collaborators</li>
                <li>• Document problematic interactions</li>
                <li>• Consult department ombudsperson or graduate advocate</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground py-8">
          <p className="mb-2">
            Content based on research from academic career resources including{' '}
            <a
              href="https://blog.ml.cmu.edu/2020/03/02/questions-to-ask-a-prospective-ph-d-advisor-on-visit-day-with-thorough-and-forthright-explanations/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline inline-flex items-center gap-1"
            >
              CMU ML Blog <ExternalLink className="h-3 w-3" />
            </a>,{' '}
            <a
              href="https://imagine.jhu.edu/blog/2024/09/27/the-art-of-the-coffee-chat-how-to-approach-best-practices-and-navigating-virtual-vs-in-person-interactions/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline inline-flex items-center gap-1"
            >
              JHU Imagine <ExternalLink className="h-3 w-3" />
            </a>, and others.
          </p>
          <Link href="/" className="text-primary hover:underline">
            ← Back to Research Advisor Finder
          </Link>
        </div>
      </div>
    </main>
  );
}
