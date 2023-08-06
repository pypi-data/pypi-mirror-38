
from collections import defaultdict
from io import StringIO
import site

from pip._vendor.distlib.metadata import Metadata
from pkg_resources import WorkingSet, find_distributions

from plover.registry import registry
from plover_plugins_manager.plugin_metadata import PluginMetadata


def recursive_get(d, *fields):
    v = d
    for name in fields:
        v = v.get(name)
        if v is None:
            break
    return v

def list_plugins():
    working_set = WorkingSet()
    # Make sure user site packages are added
    # to the set so user plugins are listed.
    user_site_packages = site.USER_SITE
    if user_site_packages not in working_set.entries:
        working_set.entry_keys.setdefault(user_site_packages, [])
        working_set.entries.append(user_site_packages)
        for dist in find_distributions(user_site_packages, only=True):
            working_set.add(dist, user_site_packages, replace=True)
    plugins = defaultdict(list)
    for dist in working_set.by_key.values():
        if dist.key == 'plover':
            continue
        is_plover_plugin = False
        for entrypoint_type in dist.get_entry_map().keys():
            if entrypoint_type.startswith('plover.'):
                is_plover_plugin = True
        if not is_plover_plugin:
            continue
        for metadata_entry in (
            'metadata.json',
            'METADATA',
            'PKG-INFO',
        ):
            if dist.has_metadata(metadata_entry):
                metadata_str = dist.get_metadata(metadata_entry)
                dist_metadata = Metadata(fileobj=StringIO(metadata_str))
                break
        else:
            continue
        metadata_dict = dist_metadata.todict()
        details = recursive_get(dist_metadata.dictionary,
                                'extensions', 'python.details')
        if details is not None:
            description_file = recursive_get(details,
                                             'document_names',
                                             'description')
            if description_file is not None and \
               dist.has_metadata(description_file):
                metadata_dict['description'] = dist.get_metadata(description_file)
            home_page = recursive_get(details,
                                      'project_urls',
                                      'Home')
            if home_page is not None:
                metadata_dict['home_page'] = home_page
            for contact in details.get('contacts', []):
                if contact['role'] == 'author':
                    metadata_dict['author'] = contact['name']
                    metadata_dict['author_email'] = contact['email']
        plugin_metadata = PluginMetadata(*[
            metadata_dict.get(k, '')
            for k in PluginMetadata._fields
        ])
        plugins[dist.key].append(plugin_metadata)
    return {
        name: list(sorted(versions))
        for name, versions in plugins.items()
    }
