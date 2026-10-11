"""Render aggregate profile statistics. Never publish tokens or repository data."""
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

QUERY = '''query ProfileCalendar($login: String!) {
  viewer { login }
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}'''

def summarize(calendar):
    days = sorted((day for week in calendar['weeks'] for day in week['contributionDays']), key=lambda d: d['date'])
    total = calendar['totalContributions']
    if not isinstance(total, int) or isinstance(total, bool) or total < 0:
        raise ValueError('Invalid contribution total.')
    dates = set()
    active = longest = current = 0
    previous = None
    for day in days:
        date = datetime.strptime(day['date'], '%Y-%m-%d').date()
        count = day['contributionCount']
        if date in dates or not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError('Invalid calendar day.')
        dates.add(date)
        if count:
            active += 1
            current = current + 1 if previous is not None and (date - previous).days == 1 else 1
            longest = max(longest, current)
        else:
            current = 0
        previous = date
    return total, active, longest

def render_stats(owner, stats):
    updated = datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="166" viewBox="0 0 900 166">',
           '<rect width="900" height="166" rx="16" fill="#eff6ff"/>',
           f'<text x="24" y="27" font-family="Arial,sans-serif" font-size="13" fill="#475569">@{escape(owner)} · Past year · Updated {updated}</text>']
    for i, (label, value) in enumerate(zip(('Contributions', 'Active days', 'Longest streak (days)'), stats)):
        x = 24 + i * 292
        svg += [f'<rect x="{x}" y="44" width="268" height="102" rx="12" fill="#ffffff" stroke="#bfdbfe"/>',
                f'<text x="{x+20}" y="77" font-family="Arial,sans-serif" font-size="14" fill="#475569">{label}</text>',
                f'<text x="{x+20}" y="122" font-family="Arial,sans-serif" font-size="34" font-weight="bold" fill="#0369a1">{value:,}</text>']
    svg.append('</svg>')
    return '\n'.join(svg)

def main():
    token = os.environ.get('GH_TOKEN', '').strip()
    owner = os.environ.get('PROFILE_OWNER', '').strip()
    if not token:
        raise ValueError('Create the PROFILE_TOKEN repository secret first. See INSTALL.md.')
    if not owner:
        raise ValueError('PROFILE_OWNER is missing.')
    request = Request('https://api.github.com/graphql',
                      data=json.dumps({'query': QUERY, 'variables': {'login': owner}}).encode(),
                      headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',
                               'User-Agent': 'profile-contribution-artwork'}, method='POST')
    with urlopen(request, timeout=45) as response:
        payload = json.load(response)
    if payload.get('errors'):
        raise ValueError('GitHub rejected the calendar query. Check PROFILE_TOKEN permissions and expiry.')
    data = payload.get('data') or {}
    viewer = (data.get('viewer') or {}).get('login', '')
    if viewer.lower() != owner.lower():
        raise ValueError('PROFILE_TOKEN must belong to the same account as the profile repository owner.')
    user = data.get('user')
    if not user:
        raise ValueError('GitHub did not return the requested user.')
    calendar = user['contributionsCollection']['contributionCalendar']
    output = Path('assets/contribution-stats.svg')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_stats(owner, summarize(calendar)), encoding='utf-8')
    print('Aggregate contribution card generated. No repository names or commit messages were exported.')

if __name__ == '__main__':
    try:
        main()
    except HTTPError as exc:
        print(f'GitHub request failed: HTTP {exc.code}. Check token permissions and expiry.', file=sys.stderr)
        sys.exit(1)
    except URLError:
        print('Could not connect to the GitHub API. Retry the workflow.', file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
