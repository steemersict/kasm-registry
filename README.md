> **Steemers Kasm Registry** — eigen registry (schema 1.1, Kasm 1.16–1.19) op `https://steemersict.github.io/kasm-registry/`.
> Plak in Kasm (Admin → Workspaces → Workspaces Registry → Add new): `https://steemersict.github.io/kasm-registry/`
>
> **Inhoud:** alleen Ferdium, met een eigen Kasm-image (`images/ferdium`, gebouwd naar `ghcr.io/steemersict/kasm-ferdium`). De eerder overgenomen LinuxServer.io-items zijn verwijderd: hun images hebben geen Kasm-entrypoint (`/kasminit`) meer en starten niet. Sjabloon: [kasmtech/workspaces_registry_template](https://github.com/kasmtech/workspaces_registry_template).
> Deploy: GitHub Actions → GitHub Pages (workflow `build-and-deploy.yml`).
>
> **Ferdium-server instellen (Kasm → Workspace → Docker Run Config Override):**
> ```json
> {"environment": {"FERDIUM_SERVER": "https://homeserver.taileb1afd.ts.net:8970"}}
> ```
> `custom_startup.sh` schrijft die waarde bij elke start in `~/.config/Ferdium/config/settings.json` (sleutel `server`, overige instellingen blijven). Zonder `FERDIUM_SERVER` verandert er niets.
> Kasm-sessies zijn niet-persistent: de waarde wordt daarom bij elke start opnieuw geschreven. `homeserver.taileb1afd.ts.net` wordt in de container al opgelost (geverifieerd in een live sessie), `extra_hosts` is niet nodig.
* **version** - This is the version of kasm the entry is compatible with
* **image** - The docker image. The tag is included for things like estimating the size and is used if there are no available_tags.
* **uncompressed_size_mb** - Integer of the approximate size of the workspace when it’s uncompressed in MB. This doesn’t take into account layers. For example if an image is 2.46GB you would enter 2460
* **available_tags** - These values are what will determine the available "channels" on the front end. If you don't want/need channels, remove the available_tags section completely. You shouldn't mix and match though, if you specify available_tags for 1 workspace, it should be specified for all of them. That doesn't mean every workspace has to have all the same tags, if a workspace only has develop tags then it will only show when develop is the selected channel. 

Head to the **Actions** tab to check your progress and once `Page build and deployment` is complete, your site should be ready.

### New Kasm Workspaces version

When a new version of Kasm is released then a new entry needs to be added to the compatibility list to support it. If you have a lot of workspaces defined then there are a couple of scripts included that can help.

Go to the processing folder and edit add_next_version.js changing the `baseversion` to match the new version. Also make sure the rest of the file matches your setup, if you anre't using channels then completely remove the `available_tags` section.

Then in a terminal run

```
cd processing
npm install
node add_next_version.js
```

This will add a new entry for every single workspace, but the size will be set to 0, this is so you can run the `get_image_sizes.js` script. This will loop through each `image` that has an uncompressed_size_mb of 0 and will pull the image, get the size, update the workspace json and remove the image. 

This can take a long time if you have a lot of workspaces and dependng on their sizes, but if the script crashes out, you can just start it agin and it will carry on from where it left off. 

```
node add_next_version.js
```

### New schema version

When a new schema version comes out, you just need to create a new branch that reflects the new schema, for example `1.2` and make it the default branch.

In the new branch, make any updates that are needed, when the changes are committed a new version will be built.

Kasm Workspaces will automatically pull the version of the schema that it understands.

If only the latest version is building (so 1.1 works but 1.0 doesn't), open build_all_branches.sh, search for `echo "All branches:` and check if there is `git fetch --all` on the line underneath, if not, add it, this will need to be added to the 1.0 branch as well if it's missing, otherwise if you make a change to 1.0 (for kasm versions 1.12.x - 1.15.x) it won't build all the branches.

**Updating to 1.16.x support**

1.16.x changed the schema from 1.0 to 1.1, the main changes to this are the compatibility changes from a simple array to an array of objects, this allows us to tie the image used and the image size to the kasm version.
In addition the top level name is removed as is top level uncompessed_size_mb as these are now available in the compatibility matrix (name is called image).

If you have an older version you will probably need to update the following files in your 1.1 branch:
* build_all_branches.sh
* processing/processjson.js
* site/components/Workspace.js
* site/pages/index.js
* site/pages/new/[[..workspace]].js

If you have a lot of workspaces (or just want an easier way to update your workspaces), there is an update file in processing called `update_1_0_to_1_1.js` copy that across to your own install, edit it and make sure the tags etc match your install. If you don't want to use channels, you can remove the available_tags section entirely.

Then to use it, create a 1.1 branch from your current 1.0 source, then in a terminal:

```
cd processing
npm install
node update_1_0_to_1_1.js
```

This will convert your existing workspaces to a 1.1 compatible format.

## Channels
Schema 1.1 added the concept of channels. Each registry can specify the channels they support, these are defined by the tags an image has. For example you might have develop, 1.16.0 and 1.16.0-rolling-daily. When the registry json is built it loops through all the workspaces and generates a list of all the possible "Channels" (tags) that are listed in compatibility.available_tags. Available tags is an optional list, if you don't include it on any of the workspaces then your registry will work as before without presenting the end user with a channels option. You shouldn't mix and match though, if you add available tags to 1 workspace, you should add available tags to all workspaces.

If you are using channels, update processing/processjson.js and specify the `default_channel` such as `'develop'`. If you aren't using channels you don't need to do anything, it will automatically detect there are no channels and set the correct value.

&nbsp;

## 6. Discovery

The tag below will hopefully make it easier for people to find your Workspace Registry by clicking on [this github search link](https://github.com/search?q=in%3Areadme+sort%3Aupdated+-user%3Akasmtech+%22KASM-REGISTRY-DISCOVERY-IDENTIFIER%22&type=repositories). If you want to make it harder to find your repository for some reason, just remove this section.

If you are the one doing the searching, click on the **site** folder, then click on **next.config.js** and the url can be found under **env.listUrl**

![search-600](https://user-images.githubusercontent.com/5698566/230614274-2976b4d7-074f-4e6d-9e58-e4d2512a3d2a.gif)

KASM-REGISTRY-DISCOVERY-IDENTIFIER


## Reporting Issues

To report any issues for this repository, please use our central issue tracker: **[Kasm Workspaces Issue Tracker](https://github.com/kasmtech/workspaces-issues/issues)**
