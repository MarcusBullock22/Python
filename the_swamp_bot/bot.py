import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN', '')
GUILD_ID = int(os.getenv('GUILD_ID', '0'))
DB = os.getenv('DATABASE_PATH', 'swamp.sqlite3')
if not TOKEN or not GUILD_ID:
    raise RuntimeError('Set DISCORD_TOKEN and GUILD_ID in .env')
GUILD = discord.Object(id=GUILD_ID)

CLASSES = {
    'Warrior': ['Arms', 'Fury', 'Protection'],
    'Shaman': ['Elemental', 'Enhancement', 'Restoration'],
    'Druid': ['Balance', 'Feral Combat', 'Restoration'],
    'Priest': ['Discipline', 'Holy', 'Shadow'],
    'Mage': ['Arcane', 'Fire', 'Frost'],
    'Warlock': ['Affliction', 'Demonology', 'Destruction'],
    'Rogue': ['Assassination', 'Combat', 'Subtlety'],
    'Hunter': ['Beast Mastery', 'Marksmanship', 'Survival'],
}
ROLES = ['Tank', 'Healer', 'DPS', 'Flex']
ROLE_NAMES = ['Swamp Council', 'Raid Leader', 'Raider', 'Swamp Dweller', 'Tadpole', 'Visitor']
CATEGORIES = {
    '🌿 THE SWAMP ENTRANCE': [('text','guild-rules'),('text','announcements'),('text','introductions'),('text','choose-your-roles')],
    '💬 THE MUD PIT': [('text','general'),('text','screenshots-and-clips'),('text','memes'),('text','addons-and-weakauras'),('voice','Swamp Lounge'),('voice','AFK')],
    '⚔️ RAIDING GROUNDS': [('text','raid-schedule'),('text','raid-signups'),('text','raid-rosters'),('text','logs-and-performance'),('text','strategies-and-guides'),('text','loot-discussion'),('voice','Raid Group 1'),('voice','Raid Group 2')],
    '🐸 SWAMP ADVENTURES': [('text','dungeons'),('text','pvp'),('text','professions-and-trading'),('text','world-buffs'),('voice','Dungeon Party 1'),('voice','Dungeon Party 2')],
    '👑 THE INNER SWAMP': [('text','officer-chat'),('text','guild-management'),('voice','Officer Meeting')],
}

def connect():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    return c

def init_db():
    with connect() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY, class_name TEXT NOT NULL,
            spec TEXT NOT NULL, raid_role TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS raids (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            starts_at TEXT NOT NULL, capacity INTEGER NOT NULL,
            channel_id INTEGER, message_id INTEGER, creator_id INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS signups (
            raid_id INTEGER NOT NULL REFERENCES raids(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL, status TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (raid_id, user_id)
        );
        ''')

def get_profile(user_id):
    with connect() as c:
        return c.execute('SELECT * FROM profiles WHERE user_id=?', (user_id,)).fetchone()

def get_raid(raid_id):
    with connect() as c:
        return c.execute('SELECT * FROM raids WHERE id=?', (raid_id,)).fetchone()

def get_signups(raid_id):
    with connect() as c:
        return c.execute('''SELECT s.*, p.class_name, p.spec, p.raid_role
          FROM signups s LEFT JOIN profiles p ON p.user_id=s.user_id
          WHERE s.raid_id=? ORDER BY s.updated_at, s.user_id''', (raid_id,)).fetchall()

def raid_embed(raid_id):
    raid = get_raid(raid_id)
    if raid is None:
        return discord.Embed(title='Raid not found')
    rows = get_signups(raid_id)
    going = [r for r in rows if r['status']=='Going']
    tentative = [r for r in rows if r['status']=='Tentative']
    declined = [r for r in rows if r['status']=='Declined']
    confirmed, waiting = going[:raid['capacity']], going[raid['capacity']:]
    when = datetime.fromisoformat(raid['starts_at'])
    stamp = int(when.timestamp())
    e = discord.Embed(title=f"⚔️ {raid['name']} · Raid #{raid_id}",
        description=f"Starts <t:{stamp}:F> (<t:{stamp}:R>)\nCapacity: **{len(confirmed)}/{raid['capacity']}** · Waitlist: **{len(waiting)}**",
        color=discord.Color.dark_green())
    def format_people(items):
        lines = [f"<@{r['user_id']}> — {r['class_name'] or '?'} / {r['spec'] or '?'} / {r['raid_role'] or '?'}" for r in items]
        result = '\n'.join(lines) or 'None'
        return result[:1000] + ('…' if len(result)>1000 else '')
    e.add_field(name=f'✅ Confirmed ({len(confirmed)})',value=format_people(confirmed),inline=False)
    e.add_field(name=f'⏳ Waitlist ({len(waiting)})',value=format_people(waiting),inline=False)
    e.add_field(name=f'❔ Tentative ({len(tentative)})',value=format_people(tentative),inline=False)
    e.add_field(name=f'❌ Declined ({len(declined)})',value=str(len(declined)),inline=True)
    e.set_footer(text='Register your class/spec/role first in #choose-your-roles. Waitlist is first-come, first-served.')
    return e

class ClassSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder='1. Select your main class', options=[discord.SelectOption(label=x) for x in CLASSES], custom_id='swamp:class')
    async def callback(self, interaction):
        cls=self.values[0]
        await interaction.response.send_message(f'Choose a specialization for **{cls}**:', view=SpecView(cls), ephemeral=True)

class ClassView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ClassSelect())

class SpecSelect(discord.ui.Select):
    def __init__(self, cls):
        self.cls=cls
        super().__init__(placeholder='2. Select your specialization', options=[discord.SelectOption(label=x) for x in CLASSES[cls]])
    async def callback(self, interaction):
        await interaction.response.send_message(f'Choose your raid role for **{self.cls} / {self.values[0]}**:',view=RaidRoleView(self.cls,self.values[0]),ephemeral=True)

class SpecView(discord.ui.View):
    def __init__(self,cls):
        super().__init__(timeout=300)
        self.add_item(SpecSelect(cls))

class RaidRoleSelect(discord.ui.Select):
    def __init__(self,cls,spec):
        self.cls,self.spec=cls,spec
        super().__init__(placeholder='3. Choose your raid role',options=[discord.SelectOption(label=r) for r in ROLES])
    async def callback(self,interaction):
        if not isinstance(interaction.user,discord.Member):
            return await interaction.response.send_message('Use this inside the guild.',ephemeral=True)
        role=self.values[0]
        with connect() as c:
            c.execute('INSERT INTO profiles(user_id,class_name,spec,raid_role) VALUES(?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET class_name=excluded.class_name,spec=excluded.spec,raid_role=excluded.raid_role', (interaction.user.id,self.cls,self.spec,role))
        # This updates primary character roles; never touches officer/admin roles.
        guild=interaction.guild
        managed_names=set(CLASSES)|set(ROLES)|{f'Spec: {c} - {s}' for c, ss in CLASSES.items() for s in ss}
        remove=[r for r in interaction.user.roles if r.name in managed_names and r.name not in (self.cls,role,f'Spec: {self.cls} - {self.spec}')]
        add=[r for r in (discord.utils.get(guild.roles,name=self.cls),discord.utils.get(guild.roles,name=role),discord.utils.get(guild.roles,name=f'Spec: {self.cls} - {self.spec}')) if r and r not in interaction.user.roles]
        try:
            if remove: await interaction.user.remove_roles(*remove,reason='Swamp Keeper profile update')
            if add: await interaction.user.add_roles(*add,reason='Swamp Keeper profile update')
            await interaction.response.send_message(f'Profile saved: **{self.cls} / {self.spec} / {role}**. Your Discord roles have been updated.',ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f'Profile saved: **{self.cls} / {self.spec} / {role}**. An officer must move the bot role above class/raid roles to enable automatic Discord role updates.',ephemeral=True)

class RaidRoleView(discord.ui.View):
    def __init__(self,cls,spec):
        super().__init__(timeout=300)
        self.add_item(RaidRoleSelect(cls,spec))

class SignupView(discord.ui.View):
    def __init__(self,raid_id):
        super().__init__(timeout=None)
        self.raid_id=raid_id
        for label,style,status in [('Going',discord.ButtonStyle.success,'Going'),('Tentative',discord.ButtonStyle.primary,'Tentative'),('Decline',discord.ButtonStyle.secondary,'Declined')]:
            button=discord.ui.Button(label=label,style=style,custom_id=f'swamp:raid:{raid_id}:{status}')
            async def handler(interaction, chosen=status):
                await self.signup(interaction,chosen)
            button.callback=handler
            self.add_item(button)
    async def signup(self,interaction,status):
        if get_raid(self.raid_id) is None:
            return await interaction.response.send_message('This raid no longer exists.',ephemeral=True)
        if status!='Declined' and get_profile(interaction.user.id) is None:
            return await interaction.response.send_message('Register your class, spec, and raid role in #choose-your-roles first.',ephemeral=True)
        with connect() as c:
            c.execute('INSERT INTO signups(raid_id,user_id,status,updated_at) VALUES(?,?,?,?) ON CONFLICT(raid_id,user_id) DO UPDATE SET status=excluded.status,updated_at=excluded.updated_at',(self.raid_id,interaction.user.id,status,datetime.now(timezone.utc).isoformat()))
        await interaction.response.send_message(f'Your signup is now **{status}**. If the raid is full, Going signups join the waitlist.',ephemeral=True)
        try:
            await interaction.message.edit(embed=raid_embed(self.raid_id),view=self)
        except (discord.Forbidden,discord.HTTPException):
            pass

intents=discord.Intents.default()
intents.members=True
bot=commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'Connected as {bot.user} (guild {GUILD_ID})')

# Automatically welcome new members with the Visitor rank.
# Requires the Server Members Intent and Manage Roles permission.
@bot.event
async def on_member_join(member: discord.Member):
    visitor = discord.utils.get(member.guild.roles, name='Visitor')
    if visitor is None:
        print(f'Visitor role not found in {member.guild.name}; run /swamp_setup.')
        return
    try:
        await member.add_roles(visitor, reason='Automatic Visitor role on join')
    except (discord.Forbidden, discord.HTTPException) as exc:
        print(f'Could not assign Visitor to {member} ({member.id}): {exc}')


# Remove Visitor whenever an officer promotes a member to a guild rank.
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    promoted_names = {'Swamp Dweller', 'Raider', 'Raid Leader', 'Swamp Council'}
    visitor = discord.utils.get(after.guild.roles, name='Visitor')
    if visitor is None or visitor not in after.roles:
        return
    # Only act when a qualifying rank was newly added (not on unrelated updates).
    before_ids = {role.id for role in before.roles}
    newly_promoted = any(
        role.name in promoted_names and role.id not in before_ids
        for role in after.roles
    )
    if not newly_promoted:
        return
    try:
        await after.remove_roles(visitor, reason='Promoted from Visitor')
    except (discord.Forbidden, discord.HTTPException) as exc:
        print(f'Could not remove Visitor from {after} ({after.id}): {exc}')


@bot.event
async def setup_hook():
    init_db()
    bot.add_view(ClassView())
    with connect() as c:
        raids=c.execute('SELECT id FROM raids WHERE message_id IS NOT NULL').fetchall()
    for raid in raids:
        bot.add_view(SignupView(raid['id']))
    await bot.tree.sync(guild=GUILD)

@bot.tree.command(name='swamp_setup',description='Create guild channels, roles and role selection menu',guild=GUILD)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def swamp_setup(interaction:discord.Interaction):
    await interaction.response.defer(ephemeral=True,thinking=True)
    guild=interaction.guild
    me=guild.me
    if not me.guild_permissions.manage_channels or not me.guild_permissions.manage_roles:
        return await interaction.followup.send('Bot requires Manage Channels and Manage Roles.',ephemeral=True)
    for name in ROLE_NAMES+list(CLASSES)+ROLES+[f'Spec: {c} - {s}' for c, ss in CLASSES.items() for s in ss]:
        if not discord.utils.get(guild.roles,name=name):
            await guild.create_role(name=name,reason='The Swamp initial setup')
    officers=[discord.utils.get(guild.roles,name=n) for n in ('Swamp Council','Raid Leader')]
    for cat_name,items in CATEGORIES.items():
        category=discord.utils.get(guild.categories,name=cat_name)
        if category is None:
            overrides={}
            if cat_name=='👑 THE INNER SWAMP':
                overrides={guild.default_role:discord.PermissionOverwrite(view_channel=False),me:discord.PermissionOverwrite(view_channel=True,send_messages=True,connect=True)}
                for officer in officers:
                    if officer: overrides[officer]=discord.PermissionOverwrite(view_channel=True,send_messages=True,connect=True)
            category=await guild.create_category(cat_name,overwrites=overrides,reason='The Swamp initial setup')
        for kind,name in items:
            exists=discord.utils.get(category.channels,name=name)
            if exists is None:
                if kind=='text': await guild.create_text_channel(name,category=category,reason='The Swamp initial setup')
                else: await guild.create_voice_channel(name,category=category,reason='The Swamp initial setup')
    # Restrict the entire raiding category to the Raider rank and guild leadership.
    # Explicitly sync existing child channels so rerunning setup updates old servers.
    raid_category = discord.utils.get(guild.categories, name='⚔️ RAIDING GROUNDS')
    if raid_category is not None:
        allowed_names = ('Raider', 'Raid Leader', 'Swamp Council')
        raid_overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            me: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_message_history=True,
                embed_links=True, connect=True, speak=True
            ),
        }
        for rank_name in allowed_names:
            rank = discord.utils.get(guild.roles, name=rank_name)
            if rank is not None:
                raid_overwrites[rank] = discord.PermissionOverwrite(
                    view_channel=True, send_messages=True,
                    read_message_history=True, connect=True, speak=True
                )
        await raid_category.edit(overwrites=raid_overwrites, reason='Raider-only channel access')
        for raid_channel in raid_category.channels:
            await raid_channel.edit(sync_permissions=True, reason='Sync Raider-only access')
    channel=discord.utils.get(guild.text_channels,name='choose-your-roles')
    # Avoid duplicate panels on repeated setup runs.
    found=False
    async for msg in channel.history(limit=100):
        if msg.author.id==bot.user.id and msg.embeds and msg.embeds[0].title=='🌿 Welcome to The Swamp':
            found=True; break
    if not found:
        e=discord.Embed(title='🌿 Welcome to The Swamp',description='Horde · WoW Forever\nSelect your **main class**, **specialization**, and **raid role** below. You can change them anytime.',color=discord.Color.dark_green())
        await channel.send(embed=e,view=ClassView())
    await interaction.followup.send('Server categories, channels, roles and self-assignment panel are ready. Run this command again safely to add missing items.',ephemeral=True)

RULE_SECTIONS = [
    ('🌿 1. Respect Your Fellow Swamp Dwellers', 'Treat members with respect. Friendly banter is welcome; harassment, discrimination, bullying, and personal attacks are not. Resolve disagreements civilly.'),
    ('⚔️ 2. Leave the Drama Outside', 'Do not stir up arguments, spread rumors, or create divisions. Handle disputes privately or ask an officer for help.'),
    ('🛡️ 3. Raiding Is a Team Effort', 'If you sign up, arrive on time and prepared with repaired gear, appropriate consumables, and encounter knowledge. Update your signup if plans change. Listen to raid leaders and give constructive feedback. **Real life comes first—communicate when possible.**'),
    ('💰 4. Loot Fairly, Play Fairly', 'Follow the announced loot rules. No ninja looting, scamming, or misleading guildmates. Bring loot disputes to officers privately.'),
    ('🐸 5. Help the Guild Grow', 'Help with quests, dungeons, professions, and questions when you can. Nobody owes anyone a carry. Be patient with newer players and do not take advantage of generosity.'),
    ('💬 6. Keep Discord Enjoyable', 'Use channels appropriately. Avoid spam, disruptive soundboards, and unnecessary mass mentions. No explicit public content, malicious links, scams, or sharing private information without permission.'),
    ('🎭 7. Keep Your Guild Roles Updated', 'Select your class, specialization, and raid role in <#1568305688571150438>. Choose Flex if you regularly fill different roles, and keep your information current.'),
    ('👑 8. Respect Guild Leadership', 'Respect officers and raid leaders during organized activities. Feedback is welcome, and leadership is held to the same rules as everyone else.'),
    ('🚫 9. No Cheating or Exploiting', "Follow WoW Forever's rules and Discord's Terms of Service. No prohibited cheating, exploiting, automation, or real-money trading that risks the guild or its members."),
    ('⚖️ 10. Common Sense Applies', 'Do not deliberately make the guild worse for others. Depending on severity, violations may lead to warnings, restrictions, or removal.'),
]

@bot.tree.command(name='post_rules', description='Publish or update the official guild rules embed', guild=GUILD)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def post_rules(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    channel = discord.utils.get(guild.text_channels, name='guild-rules')
    if channel is None:
        return await interaction.followup.send('Could not find #guild-rules. Run /swamp_setup first.', ephemeral=True)

    embeds = []
    for i in range(0, len(RULE_SECTIONS), 5):
        first = i == 0
        embed = discord.Embed(
            title='🐊 THE SWAMP — GUILD RULES',
            description=('**WoW Forever | Horde | For the Horde!**\nWelcome to The Swamp! Have fun, conquer content, collect loot, and look after your guildmates.' if first else None),
            color=discord.Color.dark_green(),
        )
        for name, value in RULE_SECTIONS:
            embed.add_field(
            name=name,
            value=value,
            inline=False
            )
            embed.set_footer(text='Have fun. Kill bosses. Get loot. Don’t be a dick. • Lok’tar Ogar!')
        embeds = [embed]

    try:
        existing = None
        async for msg in channel.history(limit=100):
            if msg.author.id == bot.user.id and msg.embeds and msg.embeds[0].title == '🐊 THE SWAMP — GUILD RULES':
                existing = msg
                break
        if existing:
            await existing.edit(embeds=embeds)
            action = 'updated'
        else:
            existing = await channel.send(embeds=embeds)
            action = 'posted'
    except discord.Forbidden:
        return await interaction.followup.send('I need View Channel, Send Messages, Embed Links, and Read Message History permissions in #guild-rules.', ephemeral=True)
    except discord.HTTPException as exc:
        return await interaction.followup.send(f'Could not publish rules: {exc}', ephemeral=True)
    await interaction.followup.send(f'Guild rules {action} in {channel.mention}: {existing.jump_url}', ephemeral=True)

@post_rules.error
async def post_rules_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        if not interaction.response.is_done():
            await interaction.response.send_message('Administrator permission required.', ephemeral=True)
    else:
        print('Post rules error:', repr(error))
        if not interaction.response.is_done():
            await interaction.response.send_message('Could not post rules. Check the bot logs.', ephemeral=True)

RAID_NAMES=['Molten Core','Onyxia','Blackwing Lair','Zul’Gurub','Ruins of Ahn’Qiraj (AQ20)','Temple of Ahn’Qiraj (AQ40)','Naxxramas','Custom']
@bot.tree.command(name='raid_create',description='Create a raid signup event (officers/raid leaders)',guild=GUILD)
@app_commands.describe(name='Raid name',starts_at='UTC date/time, e.g. 2026-11-15 01:00',capacity='Maximum confirmed players (1-40)')
@app_commands.choices(name=[app_commands.Choice(name=n,value=n) for n in RAID_NAMES])
async def raid_create(interaction:discord.Interaction,name:app_commands.Choice[str],starts_at:str,capacity:app_commands.Range[int,1,40]=40):
    member=interaction.user
    if not isinstance(member,discord.Member) or not (member.guild_permissions.administrator or any(r.name in ('Swamp Council','Raid Leader') for r in member.roles)):
        return await interaction.response.send_message('Only raid leaders and officers can create raids.',ephemeral=True)
    try:
        dt=datetime.strptime(starts_at,'%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
    except ValueError:
        return await interaction.response.send_message('Use UTC time format YYYY-MM-DD HH:MM.',ephemeral=True)
    if dt<=datetime.now(timezone.utc):
        return await interaction.response.send_message('Raid must be scheduled in the future.',ephemeral=True)
    channel=discord.utils.get(interaction.guild.text_channels,name='raid-signups')
    if channel is None:
        return await interaction.response.send_message('Run /swamp_setup first.',ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    with connect() as c:
        cur=c.execute('INSERT INTO raids(name,starts_at,capacity,creator_id) VALUES(?,?,?,?)',(name.value,dt.isoformat(),capacity,member.id))
        raid_id=cur.lastrowid
    view=SignupView(raid_id)
    try:
        message=await channel.send(embed=raid_embed(raid_id),view=view)
    except discord.HTTPException:
        with connect() as c: c.execute('DELETE FROM raids WHERE id=?',(raid_id,))
        return await interaction.followup.send('Could not post signup. Check bot permissions.',ephemeral=True)
    with connect() as c:
        c.execute('UPDATE raids SET channel_id=?,message_id=? WHERE id=?',(channel.id,message.id,raid_id))
    bot.add_view(view)
    await interaction.followup.send(f'Raid #{raid_id} posted in {channel.mention}.',ephemeral=True)

@bot.tree.command(name='raid_roster',description='View the latest roster for a raid',guild=GUILD)
async def raid_roster(interaction:discord.Interaction,raid_id:int):
    if get_raid(raid_id) is None:
        return await interaction.response.send_message('Raid not found.',ephemeral=True)
    await interaction.response.send_message(embed=raid_embed(raid_id),ephemeral=True)

@bot.tree.command(name='raid_cancel',description='Cancel a raid and remove its signup message',guild=GUILD)
async def raid_cancel(interaction:discord.Interaction,raid_id:int):
    member=interaction.user
    if not isinstance(member,discord.Member) or not (member.guild_permissions.administrator or any(r.name in ('Swamp Council','Raid Leader') for r in member.roles)):
        return await interaction.response.send_message('Only raid leaders and officers can cancel raids.',ephemeral=True)
    raid=get_raid(raid_id)
    if raid is None:
        return await interaction.response.send_message('Raid not found.',ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    if raid['channel_id'] and raid['message_id']:
        try:
            channel=bot.get_channel(raid['channel_id']) or await bot.fetch_channel(raid['channel_id'])
            message=await channel.fetch_message(raid['message_id'])
            await message.delete()
        except (discord.NotFound,discord.Forbidden,discord.HTTPException):
            pass
    with connect() as c: c.execute('DELETE FROM raids WHERE id=?',(raid_id,))
    await interaction.followup.send(f'Raid #{raid_id} canceled.',ephemeral=True)

@swamp_setup.error
async def setup_error(interaction,error):
    if isinstance(error,app_commands.MissingPermissions):
        await interaction.response.send_message('Administrator permission required.',ephemeral=True)
    else:
        print('Setup error:',repr(error))
        if not interaction.response.is_done():
            await interaction.response.send_message('Setup failed. Check the bot logs.',ephemeral=True)

bot.run(TOKEN)
