from __future__ import annotations

from decimal import Decimal
import json

import streamlit as st

from game_logic import (
    ACTIVE,
    DROPPED,
    ELIMINATED,
    REMOVED,
    GameState,
    announcement,
    check_roll,
    create_game,
    format_numbers,
    mark_player,
    update_settings,
    validate_setup,
)


st.set_page_config(
    page_title="Hot Potato Game Manager",
    page_icon="🥔",
    layout="wide",
)

st.markdown(
    """
    <style>
      .stApp { max-width: 1450px; margin: 0 auto; }
      .big-winner {
        border: 2px solid #22c55e;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        font-size: 1.35rem;
        font-weight: 700;
      }
      .number-box {
        border: 1px solid rgba(128,128,128,.35);
        border-radius: 10px;
        padding: .8rem;
        line-height: 1.8;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_all() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def initialize_setup() -> None:
    st.session_state.setdefault("game", None)
    st.session_state.setdefault("player_count", 8)
    st.session_state.setdefault("setup_names", [f"Player {i}" for i in range(1, 9)])
    st.session_state.setdefault("confirm_edit", False)
    st.session_state.setdefault("confirm_reset", False)
    st.session_state.setdefault("selected_player", None)
    st.session_state.setdefault("last_roll_result", None)


initialize_setup()
game: GameState | None = st.session_state.game

st.title("🥔 Hot Potato Game Manager")
st.caption(
    "Generate cumulative hot-potato numbers, track player outcomes, recalculate the pot, "
    "and automatically declare the winner."
)

if game is None:
    st.subheader("Game setup")
    left, right = st.columns([1, 1])

    with left:
        player_count = st.number_input(
            "Number of players",
            min_value=2,
            max_value=25,
            value=int(st.session_state.player_count),
            step=1,
        )
        player_count = int(player_count)
        st.session_state.player_count = player_count

        names = list(st.session_state.setup_names)
        if len(names) < player_count:
            names.extend(f"Player {i}" for i in range(len(names) + 1, player_count + 1))
        names = names[:player_count]

        st.markdown("**Player names**")
        updated_names = []
        columns = st.columns(2)
        for index in range(player_count):
            with columns[index % 2]:
                updated_names.append(
                    st.text_input(
                        f"Player {index + 1}",
                        value=names[index],
                        key=f"setup_player_{index}",
                    )
                )
        st.session_state.setup_names = updated_names

    with right:
        max_number = st.number_input(
            "Roll range maximum",
            min_value=1,
            max_value=999,
            value=300,
            step=1,
            help="Players roll from 1 through this number.",
        )
        initial_count = st.number_input(
            "Initial hot-potato numbers",
            min_value=1,
            max_value=int(max_number),
            value=min(25, int(max_number)),
            step=1,
        )
        add_count = st.number_input(
            "New numbers after each elimination",
            min_value=1,
            max_value=999,
            value=5,
            step=1,
        )
        entry_fee = st.number_input(
            "Fixed entry fee per player",
            min_value=0.01,
            value=10.00,
            step=1.00,
            format="%.2f",
        )
        pct_col1, pct_col2 = st.columns(2)
        with pct_col1:
            player_percentage = st.number_input(
                "Player percentage", min_value=0.0, max_value=100.0, value=70.0, step=1.0
            )
        with pct_col2:
            house_percentage = st.number_input(
                "House percentage", min_value=0.0, max_value=100.0, value=30.0, step=1.0
            )

        preview_total = Decimal(str(entry_fee)) * player_count
        preview_player = preview_total * Decimal(str(player_percentage)) / Decimal("100")
        preview_house = preview_total * Decimal(str(house_percentage)) / Decimal("100")
        st.info(
            f"Starting pot: **{preview_total:.2f}**  \n"
            f"Player payout: **{preview_player:.2f}**  \n"
            f"House payout: **{preview_house:.2f}**"
        )
        if round(player_percentage + house_percentage, 2) != 100.0:
            st.warning("Player and house percentages must total 100%.")

        if st.button("Start game", type="primary", use_container_width=True):
            errors = validate_setup(
                updated_names,
                int(max_number),
                int(initial_count),
                int(add_count),
                entry_fee,
                player_percentage,
                house_percentage,
            )
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.game = create_game(
                    updated_names,
                    int(max_number),
                    int(initial_count),
                    int(add_count),
                    entry_fee,
                    player_percentage,
                    house_percentage,
                )
                st.rerun()

else:
    # Header metrics
    active_count = len(game.active_players)
    metric_cols = st.columns(5)
    metric_cols[0].metric("Active players", active_count)
    metric_cols[1].metric("Round", game.round_number)
    metric_cols[2].metric("Active numbers", len(game.active_numbers))
    metric_cols[3].metric("Total pot", f"{game.total_pot:.2f} Gil")
    metric_cols[4].metric("Player payout", f"{game.winner_payout:.2f} Gil")

    if game.finished:
        if game.winner_name:
            st.markdown(
                f"""
                <div class="big-winner">
                    🏆 Winner: {game.winner_name}<br>
                    Payout: {game.winner_payout:.2f} Gil<br>
                    Total pot: {game.total_pot:.2f} Gil
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.balloons()
        else:
            st.error("The game ended without an active player.")

    main, sidebar = st.columns([2.1, 1])

    with main:
        st.subheader("Round announcement")
        if game.last_added_numbers:
            message = announcement(game)
        else:
            message = "No new hot potato numbers were available for this round."
        st.text_area(
            "Copy and paste",
            value=message,
            height=95,
            key=f"announcement_{game.round_number}_{len(game.active_numbers)}",
        )

        with st.expander("View all active hot-potato numbers"):
            st.markdown(
                f'<div class="number-box">{format_numbers(game.active_numbers)}</div>',
                unsafe_allow_html=True,
            )

        st.subheader("Players")
        rows = []
        for position, player in enumerate(game.players, start=1):
            rows.append(
                {
                    "Order": position,
                    "Player": player.name,
                    "Status": player.status,
                    "Entry": f"{game.entry_fee:.2f} Gil"
                    if player.status not in (DROPPED, REMOVED)
                    else "$0.00",
                    "Elimination order": player.elimination_order or "",
                }
            )

        player_table = st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="player_table",
        )

        # Clicking a row is an alternate way to choose the same player shown in the dropdown.
        selected_rows = player_table.selection.rows
        if selected_rows:
            clicked_player = game.players[selected_rows[0]]
            if clicked_player.status == ACTIVE:
                st.session_state.selected_player = clicked_player.name

        if not game.finished:
            st.subheader("Record player outcome")
            active_names = [p.name for p in game.active_players]
            if st.session_state.selected_player not in active_names:
                st.session_state.selected_player = active_names[0]

            selected_name = st.selectbox(
                "Player (choose here or click their row above)",
                active_names,
                index=active_names.index(st.session_state.selected_player),
            )
            st.session_state.selected_player = selected_name

            outcome = st.radio(
                "Outcome",
                [ELIMINATED, DROPPED, REMOVED],
                horizontal=True,
                help=(
                    "For elimination, enter the player's roll and the app will verify it. "
                    "Dropouts and removed/disqualified players do not need a roll."
                ),
            )

            if outcome == ELIMINATED:
                roll = st.number_input(
                    "Player roll",
                    min_value=1,
                    max_value=game.max_number,
                    value=1,
                    step=1,
                )
                if st.button("Check roll", type="primary", use_container_width=True):
                    try:
                        is_hot = check_roll(game, selected_name, int(roll))
                        if is_hot:
                            mark_player(game, selected_name, ELIMINATED)
                            st.session_state.last_roll_result = (
                                "error",
                                f"💥 {selected_name} rolled {int(roll)} and was eliminated.",
                            )
                        else:
                            st.session_state.last_roll_result = (
                                "success",
                                f"✅ {selected_name} rolled {int(roll)} and is safe.",
                            )
                        st.session_state.game = game
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            else:
                action_text = {
                    DROPPED: "Mark connectivity dropout",
                    REMOVED: "Remove / disqualify player",
                }[outcome]
                if st.button(action_text, type="primary", use_container_width=True):
                    try:
                        mark_player(game, selected_name, outcome)
                        st.session_state.game = game
                        st.session_state.last_roll_result = None
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))

            if st.session_state.last_roll_result:
                result_type, result_message = st.session_state.last_roll_result
                getattr(st, result_type)(result_message)

    with sidebar:
        st.subheader("Pot details")
        st.write(f"Fixed entry fee: **{game.entry_fee:.2f}** Gil")
        st.write(f"Entries remaining in pot: **{game.paid_player_count}**")
        st.write(f"Total pot: **{game.total_pot:.2f}** Gil")
        st.write(
            f"Player receives {game.player_percentage:.2f}%: **{game.winner_payout:.2f}** Gil"
        )
        st.write(
            f"House receives {game.house_percentage:.2f}%: **{game.house_payout:.2f}** Gil"
        )

        st.divider()
        st.subheader("Game controls")

        if st.button("Edit game settings", use_container_width=True):
            st.session_state.confirm_edit = True

        if st.session_state.confirm_edit:
            st.warning(
                "Changing settings during a game can affect the pot and future number generation. "
                "Existing hot-potato numbers will remain active."
            )
            edit_max = st.number_input(
                "New roll range maximum",
                min_value=1,
                max_value=999,
                value=game.max_number,
                key="edit_max",
            )
            edit_add = st.number_input(
                "New numbers per elimination",
                min_value=1,
                max_value=999,
                value=game.add_per_elimination,
                key="edit_add",
            )
            edit_fee = st.number_input(
                "New fixed entry fee",
                min_value=0.01,
                value=float(game.entry_fee),
                step=1.0,
                format="%.2f",
                key="edit_fee",
            )
            edit_player_pct = st.number_input(
                "New player percentage",
                min_value=0.0,
                max_value=100.0,
                value=float(game.player_percentage),
                step=1.0,
                key="edit_player_pct",
            )
            edit_house_pct = st.number_input(
                "New house percentage",
                min_value=0.0,
                max_value=100.0,
                value=float(game.house_percentage),
                step=1.0,
                key="edit_house_pct",
            )
            if round(edit_player_pct + edit_house_pct, 2) != 100.0:
                st.warning("Player and house percentages must total 100%.")
            confirm = st.checkbox(
                "I understand this will update the active game.",
                key="edit_confirm_checkbox",
            )
            save_col, cancel_col = st.columns(2)
            with save_col:
                if st.button(
                    "Confirm edit",
                    disabled=not confirm,
                    use_container_width=True,
                ):
                    try:
                        update_settings(
                            game,
                            int(edit_max),
                            int(edit_add),
                            edit_fee,
                            edit_player_pct,
                            edit_house_pct,
                        )
                        st.session_state.game = game
                        st.session_state.confirm_edit = False
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            with cancel_col:
                if st.button("Cancel edit", use_container_width=True):
                    st.session_state.confirm_edit = False
                    st.rerun()

        if st.button("Start a new game", use_container_width=True):
            st.session_state.confirm_reset = True

        if st.session_state.confirm_reset:
            st.error("This permanently clears the current game and its log.")
            reset_confirm = st.checkbox(
                "I want to clear this game.",
                key="reset_confirm_checkbox",
            )
            reset_col, keep_col = st.columns(2)
            with reset_col:
                if st.button(
                    "Clear game",
                    disabled=not reset_confirm,
                    use_container_width=True,
                ):
                    reset_all()
            with keep_col:
                if st.button("Keep game", use_container_width=True):
                    st.session_state.confirm_reset = False
                    st.rerun()

    st.divider()
    st.subheader("Game log")
    for entry in reversed(game.log):
        st.write(f"• {entry}")

    export_data = {
        "settings": {
            "max_number": game.max_number,
            "initial_count": game.initial_count,
            "add_per_elimination": game.add_per_elimination,
            "entry_fee": str(game.entry_fee),
            "player_percentage": str(game.player_percentage),
            "house_percentage": str(game.house_percentage),
        },
        "players": [
            {
                "name": player.name,
                "status": player.status,
                "elimination_order": player.elimination_order,
            }
            for player in game.players
        ],
        "active_numbers": game.active_numbers,
        "winner": game.winner_name,
        "total_pot": str(game.total_pot),
        "winner_payout": str(game.winner_payout),
        "log": game.log,
    }
    st.download_button(
        "Download game record",
        data=json.dumps(export_data, indent=2),
        file_name="hot_potato_game_record.json",
        mime="application/json",
    )
