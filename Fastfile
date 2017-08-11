# Customise this file, documentation can be found here:
# https://github.com/fastlane/fastlane/tree/master/fastlane/docs
# All available actions: https://github.com/fastlane/fastlane/blob/master/fastlane/docs/Actions.md
# can also be listed using the `fastlane actions` command

# Change the syntax highlighting to Ruby
# All lines starting with a # are ignored when running `fastlane`

# If you want to automatically update fastlane if a new version is available:
# update_fastlane

# This is the minimum version number required.
# Update this, if you use features of a newer version
fastlane_version "2.9.0"
build_gradle_file_path = File.expand_path("..", Dir.pwd)+"/app/build.gradle"

ENV['build_gradle_file_path'] = build_gradle_file_path
ENV['general_major_version'] = '2'

default_platform :android

platform :android do
  before_all do
    gs_android_before_all
  end

  desc "Submit a new Beta Build to Crashlytics"
  lane :beta do
    gs_android_beta
  end

  desc "Deploy a new RC version to the Google Play"
  lane :rc do
    gs_android_rc
  end

  desc "Deploy release version to Google Play"
  lane :release do
  	gs_android_release
  end

  after_all do |lane|
    gs_android_after_all(lane: lane)
  end

  error do |lane, exception|
  	gs_android_on_error(lane: lane, exception: exception)
  end
end
