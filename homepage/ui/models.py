from django.db import models
from django.utils.functional import cached_property


from django.template.loader import render_to_string
from django.utils.functional import cached_property


class Renderable:
    """Supply a mixin for in-place template rendering."""

    template_name = None

    @cached_property
    def rendered(self):
        """
        Render the object into a html string.

        A template name must be specified beforehand. The given data,
        as well as the object itself are passed to the template.
        The object's attributes are directly accessible
        in the template via model.attribute.

        Returns:
            str: The template rendered to a string.
        """
        return render_to_string(self.template_name, context={"model": self})


class Gradient(models.Model):
    color_steps = models.TextField()

    @cached_property
    def colors(self):
        return str(self.color_steps).split()

    @cached_property
    def color_start(self):
        return self.colors[0]

    @cached_property
    def color_end(self):
        return self.colors[-1]

    @cached_property
    def gradient_string(self):
        num_colors = len(self.colors)
        return ", ".join(
            ["{} {}%".format(color, 100 * (float(i) / float(num_colors - 1) if i != 0 else 0))
             for i, color in enumerate(self.colors)]
        )

    @cached_property
    def svg_gradient_id(self):
        return "svg-gradient-{id}".format(id=self.id)

    @cached_property
    def svg_stops(self):
        stops = list()
        num_colors = len(self.colors)
        for i, color in enumerate(self.colors):
            stops.append(
                '<stop offset="{offset}%" style="stop-color: {color}; stop-opacity: 1" />'.format(
                    offset=100 * (float(i) / float(num_colors - 1) if i != 0 else 0),
                    color=color
                )
            )
        return "\n".join(stops)

    @cached_property
    def svg_gradient(self):
        return """
        <linearGradient id="{svg_gradient_id}" gradientTransform="rotate(45)">  
            {svg_stops}
        </linearGradient>
        """.format(
            svg_gradient_id=self.svg_gradient_id,
            svg_stops=self.svg_stops
        )

    @cached_property
    def css_class(self):
        return "bg-gradient-{id}".format(id=self.id)

    @cached_property
    def css(self):
        return """
        .{css_class} {{
            background: {default};
            background: -moz-linear-gradient(45deg, {gradient_string});
            background: -webkit-linear-gradient(45deg,  {gradient_string});
            background: linear-gradient(45deg,  {gradient_string});
        }}
        """.format(
            css_class=self.css_class,
            default=self.colors[0],
            gradient_string=self.gradient_string
        )

    def __str__(self):
        return " -> ".join(self.colors)