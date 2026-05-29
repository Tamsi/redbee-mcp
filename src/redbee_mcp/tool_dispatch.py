"""
Tool name to handler mapping for MCP dispatch.
"""

from typing import Any, Awaitable, Callable, Dict, List

from mcp.types import TextContent

from .models import RedBeeConfig
from .tools.auth import (
    create_anonymous_session,
    login_user,
    logout_user,
    validate_session_token,
)
from .tools.content import (
    get_asset_collection_entries,
    get_asset_details,
    get_asset_thumbnail,
    get_assets_by_tag,
    get_epg_for_channel,
    get_episodes_for_season,
    get_playback_info,
    get_public_asset_details,
    get_seasons_for_series,
    list_assets,
    search_assets_autocomplete,
    search_content_v2,
    search_multi_v3,
)
from .tools.purchases import (
    add_payment_method,
    cancel_purchase_subscription,
    get_account_purchases,
    get_account_transactions,
    get_offerings,
    get_stored_payment_methods,
    purchase_product_offering,
)
from .tools.system import (
    delete_user_device_impl,
    get_active_channels_impl,
    get_system_config_impl,
    get_system_time_impl,
    get_user_devices_impl,
    get_user_location_impl,
)
from .tools.user_management import (
    add_user_profile,
    change_user_password,
    get_user_preferences,
    get_user_profiles,
    select_user_profile,
    set_user_preferences,
    signup_user,
)

ToolHandler = Callable[[RedBeeConfig, dict], Awaitable[List[TextContent]]]


async def _login_user(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await login_user(
        config=config,
        username=args["username"],
        password=args["password"],
        remember_me=args.get("remember_me", False),
    )


async def _create_anonymous_session(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await create_anonymous_session(config=config)


async def _validate_session_token(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await validate_session_token(config=config, session_token=args["session_token"])


async def _logout_user(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await logout_user(config=config, session_token=args["session_token"])


async def _search_content_v2(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await search_content_v2(
        config=config,
        query=args["query"],
        locale=args.get("locale"),
        types=args.get("types", "MOVIE,TV_SHOW"),
        tags=args.get("tags"),
        durationLower=args.get("durationLower"),
        durationUpper=args.get("durationUpper"),
        subtitles=args.get("subtitles"),
        schemes=args.get("schemes"),
        parentalRatings=args.get("parentalRatings"),
        onlyPublished=args.get("onlyPublished", True),
        allowedCountry=args.get("allowedCountry"),
        onlyDownloadable=args.get("onlyDownloadable"),
        pageSize=args.get("pageSize", 50),
        pageNumber=args.get("pageNumber", 1),
        service=args.get("service"),
        fieldSet=args.get("fieldSet", "ALL"),
        includeFields=args.get("includeFields"),
        excludeFields=args.get("excludeFields"),
    )


async def _get_asset_details(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_asset_details(
        config=config,
        assetId=args["assetId"],
        includeUserData=args.get("includeUserData", True),
    )


async def _get_playback_info(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_playback_info(
        config=config,
        assetId=args["assetId"],
        sessionToken=args["sessionToken"],
    )


async def _search_assets_autocomplete(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await search_assets_autocomplete(
        config=config,
        query=args["query"],
        fieldSet=args.get("fieldSet", "ALL"),
    )


async def _get_epg_for_channel(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_epg_for_channel(
        config=config,
        channelId=args["channelId"],
        fromDate=args.get("fromDate"),
        toDate=args.get("toDate"),
        includeUserData=args.get("includeUserData", True),
    )


async def _get_episodes_for_season(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_episodes_for_season(
        config=config,
        seasonId=args["seasonId"],
        includeUserData=args.get("includeUserData", True),
    )


async def _get_public_asset_details(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_public_asset_details(
        config=config,
        assetId=args["assetId"],
        onlyPublished=args.get("onlyPublished", True),
        fieldSet=args.get("fieldSet", "ALL"),
    )


async def _get_assets_by_tag(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_assets_by_tag(
        config,
        tagType=args.get("tagType"),
        assetType=args.get("assetType", "MOVIE"),
        onlyPublished=args.get("onlyPublished", True),
    )


async def _list_assets(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await list_assets(
        config,
        assetType=args.get("assetType"),
        assetTypes=args.get("assetTypes"),
        pageNumber=args.get("pageNumber", 1),
        pageSize=args.get("pageSize", 50),
        sort=args.get("sort"),
    )


async def _search_multi_v3(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await search_multi_v3(
        config=config,
        query=args["query"],
        types=args.get("types", "MOVIE,TV_SHOW"),
        locales=args.get("locales"),
        tags=args.get("tags"),
        schemes=args.get("schemes"),
        parentalRatings=args.get("parentalRatings"),
        pageSize=args.get("pageSize", 50),
        pageNumber=args.get("pageNumber", 1),
        onlyPublished=args.get("onlyPublished", True),
    )


async def _get_asset_collection_entries(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_asset_collection_entries(
        config=config,
        assetId=args["assetId"],
        pageSize=args.get("pageSize", 50),
        pageNumber=args.get("pageNumber", 1),
        onlyPublished=args.get("onlyPublished", True),
        fieldSet=args.get("fieldSet", "ALL"),
    )


async def _get_asset_thumbnail(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_asset_thumbnail(
        config=config,
        assetId=args["assetId"],
        time=args.get("time"),
    )


async def _get_seasons_for_series(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_seasons_for_series(
        config=config,
        assetId=args["assetId"],
        pageSize=args.get("pageSize", 50),
        pageNumber=args.get("pageNumber", 1),
        onlyPublished=args.get("onlyPublished", True),
        fieldSet=args.get("fieldSet", "ALL"),
    )


async def _signup_user(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await signup_user(
        config=config,
        username=args["username"],
        password=args["password"],
        email=args.get("email"),
        firstName=args.get("firstName"),
        lastName=args.get("lastName"),
        dateOfBirth=args.get("dateOfBirth"),
    )


async def _change_user_password(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await change_user_password(
        config=config,
        sessionToken=args["sessionToken"],
        oldPassword=args["oldPassword"],
        newPassword=args["newPassword"],
    )


async def _get_user_profiles(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_user_profiles(config=config, sessionToken=args["sessionToken"])


async def _add_user_profile(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await add_user_profile(
        config=config,
        sessionToken=args["sessionToken"],
        profileName=args["profileName"],
        dateOfBirth=args.get("dateOfBirth"),
        avatar=args.get("avatar"),
    )


async def _select_user_profile(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await select_user_profile(
        config=config,
        sessionToken=args["sessionToken"],
        profileId=args["profileId"],
    )


async def _get_user_preferences(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_user_preferences(config=config, sessionToken=args["sessionToken"])


async def _set_user_preferences(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await set_user_preferences(
        config=config,
        sessionToken=args["sessionToken"],
        preferences=args["preferences"],
    )


async def _get_account_purchases(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_account_purchases(
        config=config,
        sessionToken=args["sessionToken"],
        includeExpired=args.get("includeExpired", False),
    )


async def _get_account_transactions(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_account_transactions(config=config, sessionToken=args["sessionToken"])


async def _get_offerings(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_offerings(config=config, sessionToken=args.get("sessionToken"))


async def _purchase_product_offering(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await purchase_product_offering(
        config=config,
        sessionToken=args["sessionToken"],
        offeringId=args["offeringId"],
        paymentMethod=args.get("paymentMethod"),
    )


async def _cancel_purchase_subscription(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await cancel_purchase_subscription(
        config=config,
        sessionToken=args["sessionToken"],
        purchaseId=args["purchaseId"],
    )


async def _get_stored_payment_methods(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_stored_payment_methods(config=config, sessionToken=args["sessionToken"])


async def _add_payment_method(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await add_payment_method(
        config=config,
        sessionToken=args["sessionToken"],
        paymentMethodData=args["paymentMethodData"],
    )


async def _get_system_config(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_system_config_impl(config=config)


async def _get_system_time(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_system_time_impl(config=config)


async def _get_user_location(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_user_location_impl(config=config)


async def _get_active_channels(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_active_channels_impl(
        config=config,
        session_token=args.get("sessionToken"),
    )


async def _get_user_devices(config: RedBeeConfig, args: dict) -> List[TextContent]:
    return await get_user_devices_impl(
        config=config,
        session_token=args["sessionToken"],
    )


async def _delete_user_device(config: RedBeeConfig, args: dict) -> List[TextContent]:
    device_id = args.get("device_id") or args.get("deviceId")
    return await delete_user_device_impl(
        config=config,
        device_id=device_id,
        session_token=args["sessionToken"],
    )


TOOL_HANDLERS: Dict[str, ToolHandler] = {
    "login_user": _login_user,
    "create_anonymous_session": _create_anonymous_session,
    "validate_session_token": _validate_session_token,
    "logout_user": _logout_user,
    "search_content_v2": _search_content_v2,
    "get_asset_details": _get_asset_details,
    "get_playback_info": _get_playback_info,
    "search_assets_autocomplete": _search_assets_autocomplete,
    "get_epg_for_channel": _get_epg_for_channel,
    "get_episodes_for_season": _get_episodes_for_season,
    "get_public_asset_details": _get_public_asset_details,
    "get_assets_by_tag": _get_assets_by_tag,
    "list_assets": _list_assets,
    "search_multi_v3": _search_multi_v3,
    "get_asset_collection_entries": _get_asset_collection_entries,
    "get_asset_thumbnail": _get_asset_thumbnail,
    "get_seasons_for_series": _get_seasons_for_series,
    "signup_user": _signup_user,
    "change_user_password": _change_user_password,
    "get_user_profiles": _get_user_profiles,
    "add_user_profile": _add_user_profile,
    "select_user_profile": _select_user_profile,
    "get_user_preferences": _get_user_preferences,
    "set_user_preferences": _set_user_preferences,
    "get_account_purchases": _get_account_purchases,
    "get_account_transactions": _get_account_transactions,
    "get_offerings": _get_offerings,
    "purchase_product_offering": _purchase_product_offering,
    "cancel_purchase_subscription": _cancel_purchase_subscription,
    "get_stored_payment_methods": _get_stored_payment_methods,
    "add_payment_method": _add_payment_method,
    "get_system_config": _get_system_config,
    "get_system_time": _get_system_time,
    "get_user_location": _get_user_location,
    "get_active_channels": _get_active_channels,
    "get_user_devices": _get_user_devices,
    "delete_user_device": _delete_user_device,
}
